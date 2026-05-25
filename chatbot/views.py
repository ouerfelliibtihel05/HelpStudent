import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


def get_openai_client():
    env_path = Path(__file__).resolve().parent.parent / '.env'
    load_dotenv(env_path, override=True)
    api_key = os.environ.get('OPENAI_API_KEY')
    # If no API key is configured, return None so callers can fall back to
    # a local/offline responder for development and testing.
    if not api_key:
        return None
    # Treat common placeholder patterns (e.g. 'your-...' in .env) as missing
    if api_key.lower().startswith('your') or api_key.startswith('YOUR_'):
        return None

    base_url = os.environ.get('OPENAI_BASE_URL')
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def _send_openai_request(messages):
    client = get_openai_client()
    model = os.environ.get('OPENAI_MODEL', 'llama3-8b-8192')
    # If no client is available (missing API key), use a simple offline
    # fallback responder to allow local development without secrets.
    if client is None:
        # Find the last user message in the conversation
        last_user = ''
        for m in reversed(messages or []):
            if isinstance(m, dict) and m.get('role') == 'user' and m.get('content'):
                last_user = m.get('content')
                break
        if not last_user and messages:
            # Try other message shapes
            last = messages[-1]
            if isinstance(last, dict):
                last_user = last.get('content', '')
            else:
                last_user = str(last)

        if not last_user:
            return 'Mode offline — pas de message utilisateur trouvé.'

        return f"Mode offline — réponse simulée: {last_user}"

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
    )

    choices = getattr(response, 'choices', [])
    if not choices:
        raise ValueError('OpenAI-compatible API returned no choices.')

    message = getattr(choices[0], 'message', None)
    if not message:
        raise ValueError('OpenAI-compatible API returned an unexpected response shape.')

    return getattr(message, 'content', '') or ''


def chat_page(request):
    return render(request, 'chatbot/chat.html')


@csrf_exempt
@require_POST
def chat(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    messages = body.get('messages', [])
    if not isinstance(messages, list):
        return JsonResponse({'error': 'Messages must be an array.'}, status=400)

    try:
        reply = _send_openai_request(messages)
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=500)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)

    return JsonResponse({
        'reply': reply,
        'usage': {},
    })
