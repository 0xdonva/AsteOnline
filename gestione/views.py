from .models import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone

# Create your views here.

class AnnuncioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Articolo
    title = "Inserimento annuncio"
    form_class = AnnuncioCreateForm
    template_name = 'annuncio_create.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        return self.request.user.groups.filter(name='Venditori').exists()

    def form_valid(self, form):
        form.instance.venditore = self.request.user.username
        return super().form_valid(form)

class AnnuncioDetailView(DetailView):
    model = Articolo
    template_name = 'annuncio_detail.html'
    context_object_name = 'articolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        articolo = self.object 
        # Ottieni l'ultima offerta per l'articolo
        ultima_offerta = Offerta.objects.filter(articolo=self.object).order_by('-id').first()
        # Viene ottenuta il tempo rimanente
        ora_attuale = timezone.now()
        ora_inizio_asta = articolo.dataInizioAsta
        delta = ora_inizio_asta + timedelta(hours=articolo.durataAsta)
        tempo_restante = (delta - ora_attuale).min

        context['venditore'] = articolo.venditore
        context['id'] = articolo.id
        context['tempo_restante'] = tempo_restante
        context['ultima_offerta'] = ultima_offerta
        
        return context

class AnnuncioUpdateView(LoginRequiredMixin, UpdateView):
    model = Articolo
    form_class = AnnuncioUpdateForm
    template_name = 'annuncio_update.html'
    success_url = reverse_lazy('homepage')

class AnnuncioDeleteView(LoginRequiredMixin, DeleteView):
    model = Articolo
    template_name = 'annuncio_delete.html'
    success_url = reverse_lazy('homepage')

# View riguardanti le offerte
class OffertaCreateView(View):
    def get(self, request, articolo_id):
        articolo = get_object_or_404(Articolo, pk=articolo_id)
        form = OffertaCreateForm()
        return render(request, 'offerta_create.html', {'form': form, 'articolo': articolo})

    def post(self, request, articolo_id):
        articolo = get_object_or_404(Articolo, pk=articolo_id)
        form = OffertaCreateForm(request.POST)

        if form.is_valid():
            saldo = form.cleaned_data['saldo']
            if articolo.offerta_set.filter(saldo__gte=saldo).exists():
                form.add_error('saldo', 'L\'offerta deve essere maggiore di quelle già fatte.')
            else:
                offerta = Offerta(acquirente=request.user, articolo=articolo, saldo=saldo)
                offerta.save()
                return redirect(AnnuncioDetailView.as_view(), pk=articolo.id)

        return render(request, 'offerta_create.html', {'form': form, 'articolo': articolo})

# View riguardanti le recensioni
class RecensioneListView(ListView):
    model = Recensione
    template_name = 'recensione_list.html'
    context_object_name = 'recensioni'

    def get_queryset(self):
        venditore = User.objects.get(username=self.kwargs['venditore_username'])
        return Recensione.objects.filter(venditore=venditore)

class RecensioneCreateView(LoginRequiredMixin, CreateView):
    model = Recensione
    form_class = RecensioneCreateForm
    template_name = 'recensione_create.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Acquirenti').exists()

    def form_valid(self, form):
        venditore = User.objects.get(username=self.kwargs['venditore_username'])
        form.instance.acquirente = self.request.user
        form.instance.venditore = venditore
        success_url = f'/gestione/recensioni/{venditore_username}'
        return super().form_valid(form)

    def get_success_url(self):
        venditore_username = self.kwargs['venditore_username']
        return reverse('recensioni', kwargs={'venditore_username': venditore_username})
