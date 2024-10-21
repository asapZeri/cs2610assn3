from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('createaccount/', views.createAccount, name='createAccount'),
    path('signin/', views.signIn, name='signIn'),
    path('sessions/new/', views.signIn, name='signIn'),
    path('logout/', views.logout, name='logout'),
    path('destinations/', views.listDestinations, name='listDestinations'),
    path('destinations/new/', views.newDestination, name='newDestination'), 
    path('destinations/create/', views.createDestination, name='createDestination'),
    path('destinations/<int:destination_id>/', views.viewDestination, name='viewDestination'), 
    path('destinations/<int:destination_id>/edit/', views.editDestination, name='editDestination'),
    path('destinations/<int:destination_id>/delete/', views.deleteDestination, name='deleteDestination'),  
]

