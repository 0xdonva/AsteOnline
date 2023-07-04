from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from gestione.models import *

class VenditoreForm(UserCreationForm):
    """
    Form usato per la registrazione di un nuovo utente ed essere inserito nel gruppo dei
    Venditori.
    """
    def save(self, commit=True):
        # Viene ottenuto un riferimento all'utente
        user = super().save(commit)
        # Ricerca il gruppo che mi interessa
        g = Group.objects.get(name="Venditori") 
        # Aggiunta dell'utente al gruppo
        g.user_set.add(user)
        return user

class AcquirenteForm(UserCreationForm):
    """
    Form usato per la registrazione di un nuovo utente ed essere inserito nel gruppo dei
    Venditori.
    """
    def save(self, commit=True):
        # Viene ottenuto un riferimento all'utente
        user = super().save(commit)
        # Ricerca il gruppo che mi interessa
        g = Group.objects.get(name="Acquirenti") 
        # Aggiunta dell'utente al gruppo
        g.user_set.add(user)
        return user

    