from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest
from .Forms import StageForm
from .Forms import UtilisateurForm
from .models import Poste
from .models import Transport
from .models import Evenement
from .models import Stage,Reaction
from .models import Logement
from .models import Utilisateur
from .models import EvenementClub
from .models import EvenementSocial
from .models import Reservation
from .Forms import ReservationForm
from .Forms import StageReservationForm, TransportReservationForm, LogementReservationForm, EvenementReservationForm
from .Forms import TransportForm
from .Forms import LogementForm
from .Forms import EvenSocialForm
from .Forms import EvenclubForm




def get_comments(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    reactions = Reaction.objects.filter(poste=poste, comment__isnull=False)
    comments = [{'comment': reaction.comment, 'id': reaction.id} for reaction in reactions]
    return JsonResponse({'comments': comments})

def index(request): 
    return HttpResponse("Première application Django")

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'alamy' and password == '12345678':
            return redirect('alamy:admine')
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('alamy:page_utilisateur')
            else:
                email = request.POST.get('email')
                pass1 = request.POST.get('password1')
                pass2 = request.POST.get('password2')

                if pass1 != pass2:
                    return HttpResponse("Passwords do not match!")
                else:
                    my_user = User.objects.create_user(username=username, email=email, password=pass1)

                    utilisateur = Utilisateur.objects.create(
                        nom=username, 
                        email=email,
                        motdepasse=pass1
                    )

                    login(request, my_user)
                    return redirect('alamy:login') 

    return render(request, 'login.html')

def accueuil(request):
    return render(request, 'accueuil.html')

def listpost(request):
    return render(request, 'listpost.html')


def recharge(request):
    return render(request, 'recharge.html')

def univer(request):
    return render(request, 'univer.html')

def communication(request):
    return render(request, 'communication.html')
def iset(request):
    return render(request, 'iset.html')

def service(request):
    return render(request, 'service.html')

def jeux(request):
    return render(request, 'jeux.html')

def poste(request):
    postes = Poste.objects.filter(is_deleted=False)
    context={'postes':postes}
    return render( request,'poste.html',context )

def logements(request):
    logements = Logement.objects.all()
    return render(request, 'logement.html', {'logements': logements})
def stages(request):
    stages = Stage.objects.all()
    return render(request, 'stages.html', {'stages': stages})

from .models import Stage, Logement, Transport, EvenementClub, EvenementSocial

def filtrer(request):
    types_poste = {
        'Stage': Stage,
        'Logement': Logement,
        'Transport': Transport,
        'EvenementClub': EvenementClub,
        'EvenementSocial': EvenementSocial
    }
    regions = []

    for type_poste, modele in types_poste.items():
        if hasattr(modele, 'lieu'):
            regions.extend(modele.objects.values_list('lieu', flat=True).distinct())
        elif hasattr(modele, 'localisation'):
            regions.extend(modele.objects.values_list('localisation', flat=True).distinct())
        elif hasattr(modele, 'depart'):
            regions.extend(modele.objects.values_list('depart', flat=True).distinct())

    regions = sorted(set(regions))

    return render(request, 'filtre.html', {'regions': regions})


def resultas(request):
    region_selected = request.GET.get('region')
    type_poste_selected = request.GET.get('type_poste')
    postes = None

    if region_selected:
        postes = []
        if type_poste_selected == 'Stage' and Stage.objects.filter(lieu=region_selected).exists():
            postes.extend(Stage.objects.filter(lieu=region_selected))
        elif type_poste_selected == 'Logement' and Logement.objects.filter(localisation=region_selected).exists():
            postes.extend(Logement.objects.filter(localisation=region_selected))
        elif type_poste_selected == 'Transport' and Transport.objects.filter(depart=region_selected).exists():
            postes.extend(Transport.objects.filter(depart=region_selected))
        elif type_poste_selected == 'EvenementClub' and EvenementClub.objects.filter(lieu=region_selected).exists():
            postes.extend(EvenementClub.objects.filter(lieu=region_selected))
        elif type_poste_selected == 'EvenementSocial' and EvenementSocial.objects.filter(lieu=region_selected).exists():
            postes.extend(EvenementSocial.objects.filter(lieu=region_selected))

    return render(request, 'resultas.html', {'postes': postes, 'region_selected': region_selected})
def transport_liste(request):
    transports = Transport.objects.all()
    context = {'transports': transports}
    return render(request, 'Transport.html', context)


def evenement_liste(request):
    evenements = Evenement.objects.all()
    context = {'evenements': evenements}
    return render(request, 'Evenement.html', context)
def qui_sommes_nous(request):
    return render(request, 'QuiSommesNous.html')

def contacter(request):
    return render(request, 'contact.html')

def ajout_utilisateur(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alamy:poste')
    else:
        form = UtilisateurForm()
        utilisateurs=Utilisateur.objects.all()
    return render(request, 'Partenaire.html', {'form': form,'utilisateurs':utilisateurs})

    

@require_POST
def like_post(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    poste.likes_count += 1
    poste.save()
    return JsonResponse({'likes_count': poste.likes_count})
    


def dislike_post(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    poste.dislikes_count += 1
    poste.save()
    return JsonResponse({'dislikes_count': poste.dislikes_count})
    



@require_POST
def add_comment(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    comment = request.POST.get('comment')
    if comment:
        poste.comments = comment
        poste.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Le commentaire est vide.'})
def detail(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    return render(request, 'detail.html', {'poste': poste})

@require_POST
def ajouter_reaction(request, poste_id):
    like = 'like' in request.POST  
    dislike = 'dislike' in request.POST  
    comment = request.POST.get('comment')

    poste = get_object_or_404(Poste, pk=poste_id)

    if like:
        Reaction.objects.create(
            like=True,
            poste=poste
        )
        poste.likes_count += 1
    elif dislike:
        Reaction.objects.create(
            dislike=True,
            poste=poste
        )
        poste.dislikes_count += 1
    elif comment:
        Reaction.objects.create(
            comment=comment,
            poste=poste
        )
        poste.comments_count += 1

    poste.save()

    return redirect('alamy:detail', poste_id=poste_id)

@login_required
def page_utilisateur(request):
    username = request.user.username
    publications_utilisateur = Poste.objects.filter(utilisateur__nom=username)
    return render(request, 'page_utilisateur.html', {'publications_utilisateur': publications_utilisateur})

def modify_post(request, poste_id):
    poste = Poste.objects.get(pk=poste_id)

    
    if request.method == 'POST':
        poste.type = request.POST.get('type')
        new_image = request.FILES.get('image')
        if new_image:
            poste.image = new_image
        try:
            stage = poste.stage
            stage.typeStg = request.POST.get('typeStg')
            stage.societe = request.POST.get('societe')
            stage.duree = request.POST.get('duree')
            stage.sujet = request.POST.get('sujet')
            stage.description = request.POST.get('description')
            stage.lieu = request.POST.get('lieu')
            stage.save()
        except ObjectDoesNotExist:
            pass
        
        try:
            evenement = poste.evenement
            evenement.intitule = request.POST.get('intitule')
            evenement.description = request.POST.get('description')
            evenement.date = request.POST.get('date')
            evenement.lieu = request.POST.get('lieu')
            evenement.contactinfo = request.POST.get('contactinfo')
            evenement.nombretickets = request.POST.get('nombretickets')
            evenement.save()
        except ObjectDoesNotExist:
            pass
        
        try:
            logement = poste.logement
            logement.localisation = request.POST.get('localisation')
            logement.description = request.POST.get('description')
            logement.nombreTables = request.POST.get('nombreTables')
            logement.contactinfo = request.POST.get('contactinfo')
            logement.save()
        except ObjectDoesNotExist:
            pass
        
        try:
            transport = poste.transport
            transport.depart = request.POST.get('depart')
            transport.destination = request.POST.get('destination')
            transport.heuredep = request.POST.get('heuredep')
            transport.nombreplaces = request.POST.get('nombreplaces')
            transport.contactinfo = request.POST.get('contactinfo')
            transport.save()
        except ObjectDoesNotExist:
            pass

        poste.save()
        
        return redirect('alamy:page_utilisateur')  

    return render(request, 'modify_post.html', {'poste': poste})


def delete_post(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    
    if request.method == 'POST':
        poste.delete() 
        return redirect('alamy:page_utilisateur')
    
    return render(request, 'delete_post.html', {'poste': poste})
     
@require_POST
def supprimer_poste(request, admine_id):
    admine = Poste.objects.get(id=admine_id)
    admine.delete()
    return redirect('alamy:admine')

@require_POST
def supprimer_user(request, admine_id):
    admine = Utilisateur.objects.get(id=admine_id)
    admine.delete()
    return redirect('alamy:ListePartenaire')
def admine(request):
    admines = Poste.objects.all()
    context = {'admines': admines}
    return render(request, 'admine.html', context)
def ListePartenaire(request):
    ListePartenaires = Utilisateur.objects.all()
    context = {'ListePartenaires': ListePartenaires}
    return render(request, 'ListePartenaire.html', context)
def qui_sommes_nous_admin(request):
    return render(request, 'QuiSommesNousadmin.html')

def qui_sommes_nous_admin(request):
    return render(request, 'QuiSommesNousadmin.html')

def filtreadmin(request):
    types_poste = {
        'Stage': Stage,
        'Logement': Logement,
        'Transport': Transport,
        'EvenementClub': EvenementClub,
        'EvenementSocial': EvenementSocial
    }
    regions = []

    for type_poste, modele in types_poste.items():
        if hasattr(modele, 'lieu'):
            regions.extend(modele.objects.values_list('lieu', flat=True).distinct())
        elif hasattr(modele, 'localisation'):
            regions.extend(modele.objects.values_list('localisation', flat=True).distinct())
        elif hasattr(modele, 'depart'):
            regions.extend(modele.objects.values_list('depart', flat=True).distinct())

    regions = sorted(set(regions))

    return render(request, 'filtreadmin.html', {'regions': regions})


def resultasadmin(request):
    region_selected = request.GET.get('region')
    type_poste_selected = request.GET.get('type_poste')
    postes = None

    if region_selected:
        postes = []
        if type_poste_selected == 'Stage' and Stage.objects.filter(lieu=region_selected).exists():
            postes.extend(Stage.objects.filter(lieu=region_selected))
        elif type_poste_selected == 'Logement' and Logement.objects.filter(localisation=region_selected).exists():
            postes.extend(Logement.objects.filter(localisation=region_selected))
        elif type_poste_selected == 'Transport' and Transport.objects.filter(depart=region_selected).exists():
            postes.extend(Transport.objects.filter(depart=region_selected))
        elif type_poste_selected == 'EvenementClub' and EvenementClub.objects.filter(lieu=region_selected).exists():
            postes.extend(EvenementClub.objects.filter(lieu=region_selected))
        elif type_poste_selected == 'EvenementSocial' and EvenementSocial.objects.filter(lieu=region_selected).exists():
            postes.extend(EvenementSocial.objects.filter(lieu=region_selected))

    return render(request, 'resultasadmin.html', {'postes': postes, 'region_selected': region_selected})



@login_required
def ajouter_stage(request):
    if request.method == 'POST':
        form = StageForm(request.POST, request.FILES, utilisateur=request.user)
        if form.is_valid():
            stage = form.save(commit=False)
            utilisateur = Utilisateur.objects.filter(nom=request.user.username).first()
            if utilisateur:
                stage.utilisateur = utilisateur
                stage.save()
                return redirect('alamy:page_utilisateur')
            else:
                pass
    else:
        form = StageForm(utilisateur=request.user)
    return render(request, 'ajouter_stage.html', {'form': form})



@login_required
def ajouter_transport(request):
    if request.method == 'POST':
        form = TransportForm(request.POST, request.FILES, utilisateur=request.user)
        if form.is_valid():
            transport = form.save(commit=False)
            utilisateur = Utilisateur.objects.filter(nom=request.user.username).first()
            if utilisateur:
                transport.utilisateur = utilisateur
                transport.save()
                return redirect('alamy:page_utilisateur')
            else:
                
                pass
    else:
        form = TransportForm(utilisateur=request.user)
    return render(request, 'ajouter_transport.html', {'form': form})


@login_required
def ajouter_logement(request):
    if request.method == 'POST':
        form = LogementForm(request.POST, request.FILES, utilisateur=request.user)
        if form.is_valid():
            logement = form.save(commit=False)
            utilisateur = Utilisateur.objects.filter(nom=request.user.username).first()
            if utilisateur:
                logement.utilisateur = utilisateur
                logement.save()
                return redirect('alamy:page_utilisateur')
            else:
            
                pass
    else:
        form = LogementForm(utilisateur=request.user)
    return render(request, 'ajouter_logement.html', {'form': form})




@login_required
def ajouter_even_soc(request):
    if request.method == 'POST':
        form = EvenSocialForm(request.POST, request.FILES, utilisateur=request.user)
        if form.is_valid():
            evensoc = form.save(commit=False)
            utilisateur = Utilisateur.objects.filter(nom=request.user.username).first()
            if utilisateur:
                evensoc.utilisateur = utilisateur
                evensoc.save()
                return redirect('alamy:page_utilisateur')
            else:
                
                pass
    else:
        form = EvenSocialForm(utilisateur=request.user)
    return render(request, 'ajouter_even_soc.html', {'form': form})



@login_required
def ajouter_even_club(request):
    if request.method == 'POST':
        form = EvenclubForm(request.POST, request.FILES, utilisateur=request.user)
        if form.is_valid():
            evenclub = form.save(commit=False)
            utilisateur = Utilisateur.objects.filter(nom=request.user.username).first()
            if utilisateur:
                evenclub.utilisateur = utilisateur
                evenclub.save()
                return redirect('alamy:page_utilisateur')
            else:
               
                pass
    else:
        form = EvenclubForm(utilisateur=request.user)
    return render(request, 'ajouter_even_club.html', {'form': form})





def reserver_poste(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    form = None

    if hasattr(poste, 'stage'):
        form = StageReservationForm(request.POST or None)
    elif hasattr(poste, 'logement'):
        form = LogementReservationForm(request.POST or None)
    elif hasattr(poste, 'transport'):
        form = TransportReservationForm(request.POST or None)
    elif hasattr(poste, 'evenement'):
        form = EvenementReservationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.poste = poste
            
           
            if hasattr(poste, 'evenement') and poste.evenement.nombretickets is not None:
                if reservation.nombre_tickets > poste.evenement.nombretickets:
                    message = 'Impossible de réserver, nombre de tickets insuffisant.'
                    alert_html = render_to_string('reservation_alert.html', {'message': message})
                    return HttpResponseBadRequest(alert_html)
            elif hasattr(poste, 'logement') and poste.logement.nombreTables is not None:
                if reservation.nombre_tables > poste.logement.nombreTables:
                    message = 'Impossible de réserver, nombre de places insuffisant.'
                    alert_html = render_to_string('reservation_alert.html', {'message': message})
                    return HttpResponseBadRequest(alert_html)
            elif hasattr(poste, 'transport') and poste.transport.nombreplaces is not None:
                if reservation.nombre_places > poste.transport.nombreplaces:
                    message = 'Impossible de réserver, nombre de places insuffisant.'
                    alert_html = render_to_string('reservation_alert.html', {'message': message})
                    return HttpResponseBadRequest(alert_html)
            
           
            reservation.save()

           
            if hasattr(poste, 'evenement') and poste.evenement.nombretickets is not None:
                poste.evenement.nombretickets -= reservation.nombre_tickets
                poste.evenement.save()
            elif hasattr(poste, 'logement') and poste.logement.nombreTables is not None:
                poste.logement.nombreTables -= reservation.nombre_tables
                poste.logement.save()
            elif hasattr(poste, 'transport') and poste.transport.nombreplaces is not None:
                poste.transport.nombreplaces -= reservation.nombre_places
                poste.transport.save()
            message = 'Réservation effectuée avec succès.'
            alert_html = render_to_string('resrve_success.html', {'message': message})
            return HttpResponseBadRequest(alert_html)
        return redirect('alamy:poste')


    return render(request, 'reserver_poste.html', {'poste': poste, 'form': form})
@login_required
def voir_reservations_poste(request, poste_id):
    poste = get_object_or_404(Poste, id=poste_id)
    reservations = Reservation.objects.filter(poste=poste)
    reservations_non_vide = []
    
    for reservation in reservations:
        reservation_fields = reservation._meta.get_fields()
        reservation_dict = {}
        for field in reservation_fields:
            field_name = field.name
            field_value = getattr(reservation, field_name)
            if field_value:
                reservation_dict[field_name] = field_value
        if reservation_dict:
            reservations_non_vide.append(reservation_dict)
    
    return render(request, 'voir_reservations_poste.html', {'poste': poste, 'reservations': reservations_non_vide})
@login_required
def modify_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    form = ReservationForm(instance=reservation)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
        return redirect('alamy:voir_reservations_poste', poste_id=reservation.poste.id)
    return render(request, 'modify_reservation.html', {'form': form})

@require_POST
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('alamy:voir_reservations_poste', poste_id=reservation.poste.id)
