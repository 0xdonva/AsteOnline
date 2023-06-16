from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import *
from gestione.models import *

class UtenteCreate(CreateView):

    model = Utente
    fields = ('email', 'username', 'password', 'is_venditore')
    form_class = UtenteForm
    template_name = 'registration.html'

class LoginView(FormView):
    
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = make_password(form.cleaned_data['password'])
        user = authenticate(username=username, password=password)

        if user is not None:
           login(self.request, user)
           return HttpResponseRedirect(self.success_url)
        else:
           return self.form_invalid(form)
