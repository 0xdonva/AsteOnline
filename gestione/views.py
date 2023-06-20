from .models import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponse

# Create your views here.

class CreateAnnuncioView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Articolo
    title = "Inserimento annuncio"
    form_class = CreateAnnuncioForm
    template_name = 'createAnnuncio.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        return self.request.user.groups.filter(name='Venditori').exists()

    def form_valid(self, form):
        form.instance.venditore = self.request.user.username
        return super().form_valid(form)

class AnnuncioListView(ListView):
    model = Articolo
    template_name = 'annuncio_list.html'
    context_object_name = 'articoli'

class AnnuncioUpdateView(LoginRequiredMixin, UpdateView):
    model = Articolo
    form_class = AnnuncioForm
    template_name = 'annuncio_update.html'
    success_url = reverse_lazy('homepage')

class AnnuncioDeleteView(LoginRequiredMixin, DeleteView):
    model = Articolo
    template_name = 'annuncio_delete.html'
    success_url = reverse_lazy('homepage')