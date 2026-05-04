from django.urls import path   
from . import views
app_name = 'alamy'
urlpatterns = [	


 path('listpost', views.listpost,name='listpost'),
    path('recharge', views.recharge,name='recharge'),
    path('univer', views.univer,name='univer'),
    path('communication', views.communication,name='communication'),
    path('get_comments/<int:poste_id>/', views.get_comments, name='get_comments'),
    path('login', views.login_user,name='login'),
    path('service', views.service,name='service'),
    path('iset', views.iset,name='iset'),
    path('index', views.index, name='index'),
    path('accueuil',views.accueuil,name='accueuil'),
     path('jeux',views.jeux,name='jeux'),
    path('',views.poste,name='poste'),
    path('logement',views.logements,name='logement'),
    path('stage',views.stages,name='stage'),
    path('filtre/',views.filtrer,name='filtre'),
    path('resultas/',views.resultas,name='resultas'),
     path('transport', views.transport_liste, name='transport'),
    path('evenement', views.evenement_liste, name='evenement'),
    path('qui-sommes-nous/', views.qui_sommes_nous, name='qui_sommes_nous'),
    path('contacter/', views.contacter, name='contact'),
    path('ajout-utilisateur/', views.ajout_utilisateur, name='ajout_utilisateur'),
    path('like-post/<int:poste_id>/', views.like_post, name='like_post'),
    path('dislike-post/<int:poste_id>/', views.dislike_post, name='dislike_post'),
    path('add-comment/<int:poste_id>/', views.add_comment, name='add_comment'),
    path('poste/<int:poste_id>/', views.detail, name='detail'),
     path('ajouter_reaction/<int:poste_id>/', views.ajouter_reaction, name='ajouter_reaction'),
     path('page_utilisateur/', views.page_utilisateur, name='page_utilisateur'),
      path('modify/<int:poste_id>/', views.modify_post, name='modify_post'),
    path('delete/<int:poste_id>/', views.delete_post, name='delete_post'),
    path('admine', views.admine,name='admine'),
path('ListePartenaire',views.ListePartenaire,name='ListePartenaire'),

path('qui-sommes-nous_admin/', views.qui_sommes_nous_admin, name='qui_sommes_nous_admin'),

path('supprimer_poste/<int:admine_id>/', views.supprimer_poste, name='supprimer_poste'),
    path('supprimer_user/<int:admine_id>/', views.supprimer_user, name='supprimer_user'),
path('filtreadmin/',views.filtreadmin,name='filtreadmin'),
path('resultasadmin/',views.resultasadmin,name='resultasadmin'),
path('ajouter_stage/', views.ajouter_stage, name='ajouter_stage'),
path('ajouter_transport/', views.ajouter_transport, name='ajouter_transport'),
path('ajouter_logement/', views.ajouter_logement, name='ajouter_logement'),
path('ajouter_even_soc/', views.ajouter_even_soc, name='ajouter_even_soc'),
path('ajouter_even_club/', views.ajouter_even_club, name='ajouter_even_club'),
path('reserver_poste/<int:poste_id>/', views.reserver_poste, name='reserver_poste'),
path('voir_reservations_poste/<int:poste_id>/', views.voir_reservations_poste, name='voir_reservations_poste'),
path('modify_reservation/<int:reservation_id>/', views.modify_reservation, name='modify_reservation'),
path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),







   




  ]
