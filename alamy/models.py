from django.db import models


class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    motdepasse = models.CharField(max_length=100,default='')  

    def __str__(self):
        return f" {self.nom}  {self.prenom} {self.telephone} {self.email} "

class Poste(models.Model):
    TYPE_CHOICES = [
        (0, 'Offre'),
        (1, 'Demande'),
    ]

    type = models.IntegerField(choices=TYPE_CHOICES)
    image = models.ImageField(null=True, blank=True)
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, null=True)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} {self.image} {self.utilisateur}"

class Evenement(Poste):
    intitule = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    date = models.DateField()
    lieu = models.CharField(max_length=100)
    contactinfo = models.CharField(max_length=100)
    nombretickets = models.IntegerField(blank=True, null=True)
    def save(self, *args, **kwargs):
            if self.nombretickets == 0:
              self.is_deleted = True
            super(Evenement, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.intitule} {self.description} {self.date} {self.lieu} {self.contactinfo} { self.nombretickets}"



class Reaction(models.Model):
    
    like = models.BooleanField(default=False, null=True)  
    dislike = models.BooleanField(default=False, null=True)
    
    comment = models.TextField(default=False, null=True)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE)



    def __str__(self):
     return f"  {self.like} {self.dislike} {self.comment} {self.poste} "


class Stage(Poste):
    TYPE_CHOICES = [
        (1, 'Ouvrier'),
        (2, 'Technicien'),
        (3, 'PFE'),
    ]
    typeStg = models.IntegerField(choices=TYPE_CHOICES)
    societe = models.CharField(max_length=100)
    duree = models.IntegerField()
    sujet = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    lieu = models.CharField(max_length=100, default='')


    def __str__(self):
     return f"{self.typeStg} {self.societe} {self.duree} {self.sujet} {self.description} {self.lieu} "

class Logement(Poste):
    localisation = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null='true')

    contactinfo = models.CharField(max_length=100)
    nombreTables = models.IntegerField(blank=True, null=True)
    def save(self, *args, **kwargs):
            if self.nombreTables== 0:
              self.is_deleted = True
            super(Logement, self).save(*args, **kwargs)

    
    def __str__(self):
     return f" {self.localisation} {self.contactinfo} {self.description} {self. nombreTables} "


class Transport(Poste):
    depart = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    heuredep = models.TimeField()
    contactinfo = models.CharField(max_length=100)
    nombreplaces = models.IntegerField(blank=True, null=True)
    def save(self, *args, **kwargs):
            if self.nombreplaces == 0:
              self.is_deleted = True
            super(Transport, self).save(*args, **kwargs)


    def __str__(self):
     return f" {self.depart} {self.destination} {self.heuredep}  {self.contactinfo}{self.nombreplaces} "

class Recommandation(Poste):
    texte = models.CharField(max_length=255)

    def __str__(self):
     return f" {self.texte} "

class EvenementClub(Evenement):
    club = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.club}"

class EvenementSocial(Evenement):
    prix = models.FloatField()
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prix} {self.specialite}"
class Reservation(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    
    date_rendez_vous = models.DateField(blank=True, null=True)
    nombre_places = models.IntegerField(blank=True, null=True)
    telephone = models.CharField(max_length=20)
    date = models.DateField(blank=True, null=True)
    heure = models.TimeField(blank=True, null=True)
    nombre_Tables4 = models.IntegerField(blank=True, null=True)
    nombre_tickets = models.IntegerField(blank=True, null=True)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE, related_name='reservation')


    def __str__(self):
        return f"Reservation for {self.poste} by {self.prenom} {self.nom}  {self.email}  {self.telephone}  {self.date}  {self. date_rendez_vous} {self.nombre_Tables4} {self.  nombre_tickets} { self.nombre_places}{self.heure}  "




 

