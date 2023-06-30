"""
URL configuration for AsteOnline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'gestione'

urlpatterns = [
    #Parte legata al venditore
    path('ricerca/', views.AnnuncioSearchView.as_view(), name = 'annuncio-search'),
    path('nuovo_annuncio/', views.AnnuncioCreateView.as_view(), name = 'annuncio-create'),
    path('annuncio/<int:pk>/', views.AnnuncioDetailView.as_view(), name='annuncio-detail'),
    path('annuncio/<int:pk>/update/', views.AnnuncioUpdateView.as_view(), name='annuncio-update'),
    path('annuncio/<int:pk>/delete/', views.AnnuncioDeleteView.as_view(), name='annuncio-delete'),

    path('nuova_offerta/<articolo_id>/', views.OffertaCreateView.as_view(), name='offerta-create'),

    path('recensioni/<venditore_username>/', views.RecensioneListView.as_view(), name = 'recensione-list'),
    path('nuova_recensione/<venditore_username>/', views.RecensioneCreateView.as_view(), name='recensione-create'),
]