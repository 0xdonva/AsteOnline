from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, TemplateView
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

class UtenteCreate(TemplateView):
    template_name = 'preregistration.html'

class HomeView(ListView):
    model = Articolo
    template_name = 'home.html'
    context_object_name = 'articoli'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            group = Group.objects.get(name='Venditori')
            is_venditore = group in user.groups.all()
            context['is_venditore'] = is_venditore
            if is_venditore:
                context['username'] = self.request.user.username
        return context