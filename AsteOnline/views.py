from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import *
from gestione.models import *

class AcquirenteCreate(CreateView):

    form_class = AcquirenteForm
    template_name = 'registration.html'
    success_url = "/login/"

class VenditoreCreate(CreateView):

    form_class = VenditoreForm
    template_name = 'registration.html'
    success_url = "/login/"

class HomeView(ListView):
    model = Articolo
    template_name = 'home.html'
    context_object_name = 'articoli'