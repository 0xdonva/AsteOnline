from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from gestione.models import *

class VenditoreForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit) #ottengo un riferimento all'utente
        g = Group.objects.get(name="Venditori") #cerco il gruppo che mi interessa
        g.user_set.add(user) #aggiungo l'utente al gruppo
        return user

class AcquirenteForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit) #ottengo un riferimento all'utente
        g = Group.objects.get(name="Acquirenti") #cerco il gruppo che mi interessa
        g.user_set.add(user) #aggiungo l'utente al gruppo
        return user

    