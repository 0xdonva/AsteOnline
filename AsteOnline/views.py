from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import *
from gestione.models import *

class VenditoreCreate(CreateView):

    model = Venditore
    fields = ('username', 'email', 'password', 'via', 'numCivico', 'CAP')
    template_name = 'registration.html'

class AcquirenteCreate(CreateView):

    model = Acquirente
    fields = ('username', 'email', 'password', 'via', 'numCivico', 'CAP')
    form = AcquirenteForm
    template_name = 'registration.html'