from django.forms import ModelForm 
from django import forms
from .models import Poste,Reaction
from .models import Utilisateur,Stage,Reservation
from .models import Transport
from .models import Logement
from .models import EvenementClub
from .models import EvenementSocial
from .models import Poste
from .models import Reservation 

class PosteForm(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ['type', 'image', 'utilisateur']
        
class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'telephone', 'email', 'motdepasse']
class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['like', 'dislike', 'comment']
        widgets = {
            'like': forms.HiddenInput(),
            'dislike': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'placeholder': 'Ajouter un commentaire'}),
        }
class StageForm(forms.ModelForm):
    type = forms.ChoiceField(choices=Poste.TYPE_CHOICES)
    image = forms.ImageField(required=False)

    class Meta:
        model = Stage
        fields = ['typeStg', 'societe', 'duree', 'sujet', 'description', 'lieu', 'type', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('utilisateur', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['utilisateur'] = forms.ModelChoiceField(queryset=Utilisateur.objects.filter(nom=user.username))
        self.fields['type'].widget = forms.Select(choices=[(0, 'Offre'), (1, 'Demande')])
        

class TransportForm(forms.ModelForm):
    type = forms.ChoiceField(choices=Poste.TYPE_CHOICES)
    image = forms.ImageField(required=False)

    class Meta:
        model = Transport
        fields = ['depart', 'destination', 'heuredep', 'contactinfo', 'type', 'image','nombreplaces']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('utilisateur', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['utilisateur'] = forms.ModelChoiceField(queryset=Utilisateur.objects.filter(nom=user.username))
        self.fields['type'].widget = forms.Select(choices=[(0, 'Offre'), (1, 'Demande')])


class LogementForm(forms.ModelForm):
    type = forms.ChoiceField(choices=Poste.TYPE_CHOICES)
    image = forms.ImageField(required=False)

    class Meta:
        model = Logement
        fields = ['localisation', 'description', 'contactinfo', 'type', 'image','nombreTables']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('utilisateur', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['utilisateur'] = forms.ModelChoiceField(queryset=Utilisateur.objects.filter(nom=user.username))
        self.fields['type'].widget = forms.Select(choices=[(0, 'Offre'), (1, 'Demande')])


class EvenSocialForm(forms.ModelForm):
    type = forms.ChoiceField(choices=Poste.TYPE_CHOICES)
    image = forms.ImageField(required=False)

    class Meta:
        model = EvenementSocial
        fields = ['type', 'image', 'intitule', 'description', 'date', 'lieu', 'contactinfo', 'prix', 'specialite','nombretickets']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('utilisateur', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['utilisateur'] = forms.ModelChoiceField(queryset=Utilisateur.objects.filter(nom=user.username))
        self.fields['type'].widget = forms.Select(choices=Poste.TYPE_CHOICES)




class EvenclubForm(forms.ModelForm):
    type = forms.ChoiceField(choices=Poste.TYPE_CHOICES)
    image = forms.ImageField(required=False)

    class Meta:
        model = EvenementClub
        fields = ['type', 'image', 'intitule', 'description', 'date', 'lieu', 'contactinfo', 'club','nombretickets']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('utilisateur', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['utilisateur'] = forms.ModelChoiceField(queryset=Utilisateur.objects.filter(nom=user.username))
        self.fields['type'].widget = forms.Select(choices=Poste.TYPE_CHOICES)


class StageReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'prenom', 'email', 'telephone', 'date_rendez_vous']
        widgets = {
            'date_rendez_vous': forms.DateInput(attrs={'type': 'date'}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
        }

class TransportReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'prenom', 'email', 'telephone', 'nombre_places']

class LogementReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'prenom', 'email', 'telephone', 'date','heure','nombre_Tables4']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
        }

class EvenementReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'prenom', 'email', 'telephone', 'nombre_tickets']
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'prenom', 'email', 'date_rendez_vous', 'nombre_places', 'heure', 'nombre_Tables4', 'nombre_tickets']
        widgets = {
            'date_rendez_vous': forms.DateInput(attrs={'type': 'date'}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
        }
