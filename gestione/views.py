from .models import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

import re

# Costanti
CATEGORIE = ['Elettronica', 'Informatica', 'CD e Vinili', 'Videogiochi', 'Strumenti musicali', 'Film e DVD']

# View

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

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.venditore = self.request.user.username
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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

        if str(articolo.dataFineAsta - timezone.now())[0] == '-':
            context['tempo_restante'] = 0
            # notifica_email(articolo)   # Vera notifica email
            print_email_falsa(articolo)  # Falsa notifica email
            articolo.terminato = True
            articolo.save()
        else:
            context['tempo_restante'] = round((articolo.dataFineAsta - timezone.now()).seconds / 60)
        context['ultima_offerta'] = ultima_offerta
        context['username'] = self.request.user.username

        articoli_consigliati = Articolo.objects.filter(
            Q(titolo__icontains=articolo.id) | Q(categoria=articolo.categoria, prezzoIniziale__range=[articolo.prezzoIniziale-20, articolo.prezzoIniziale+20])
        ).exclude(id=articolo.id)[:3]
        context['articoli_consigliati'] = articoli_consigliati
        
        return context

class AnnuncioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articolo
    form_class = AnnuncioUpdateForm
    template_name = 'annuncio_update.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        # Verifica se l'utente corrente è il venditore dell'articolo
        articolo = self.get_object()
        return articolo.venditore == self.request.user.username


class AnnuncioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articolo
    template_name = 'annuncio_delete.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        # Verifica se l'utente corrente è il venditore dell'articolo
        articolo = self.get_object()
        return articolo.venditore == self.request.user.username

class AnnuncioSearchView(ListView):
    model = Articolo
    template_name = 'annuncio_search.html'
    context_object_name = 'articoli'

    def get_queryset(self):
        query = self.request.GET.get('q')  # Ottieni il valore della query dalla richiesta GET
        if query:
            return Articolo.objects.filter(titolo__icontains=query)  # Filtra gli articoli per il titolo che contiene la query
        else:
            return Articolo.objects.all()  # Restituisci tutti gli articoli se la query non è presente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')  # Passa il valore della query al contesto del template
        return context

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
                return redirect('gestione:annuncio-detail', pk=articolo.id)

        return render(request, 'offerta_create.html', {'form': form, 'articolo': articolo})

# View riguardanti le recensioni
class RecensioneListView(ListView):
    model = Recensione
    template_name = 'recensione_list.html'
    context_object_name = 'recensioni'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venditore = self.kwargs['venditore_username']
        articoli = Articolo.objects.filter(venditore=venditore)
        context['articoli'] = articoli
        context['venditore'] = venditore
        return context

    def get_queryset(self):
        venditore = User.objects.get(username=self.kwargs['venditore_username'])
        return Recensione.objects.filter(venditore=venditore)

class RecensioneCreateView(LoginRequiredMixin, CreateView):
    model = Recensione
    form_class = RecensioneCreateForm
    template_name = 'recensione_create.html'

    def test_func(self):
        # Metodo che controlla se l'utente appartiene al gruppo 'Acquirenti'
        return self.request.user.groups.filter(name='Acquirenti').exists()

    def form_valid(self, form):
        # Metodo chiamato quando il form è valido
        venditore = User.objects.get(username=self.kwargs['venditore_username'])
        form.instance.acquirente = self.request.user
        form.instance.venditore = venditore
        return super().form_valid(form)

    def get_success_url(self):
        # Metodo che restituisce l'URL di successo dopo la creazione della recensione
        venditore_username = self.kwargs['venditore_username']
        return reverse('gestione:recensione-list', kwargs={'venditore_username': venditore_username})

## Funzione per la notifica email al vincitore dell'asta
#def notifica_email(articolo):
#    offerta = Offerta.objects.filter(articolo=articolo).order_by('-importo').first()
#    if offerta_piu_alta:
#        # Ottieni l'utente vincitore dell'asta
#        vincitore = offerta_piu_alta.utente
#
#        # Invia la mail al vincitore
#        subject = f"Complimenti! Hai vinto l'asta per l'articolo {articolo.titolo}"
#        message = f"Ciao {vincitore.username},\n\nHai vinto l'asta per l'articolo {articolo.titolo}.\n\nGrazie per aver partecipato!\n\nCordiali saluti,\nIl Tuo Sito"
#        sender = 'your-email@example.com'
#        receiver = vincitore.email
#
#        msg = MIMEText(message)
#        msg['Subject'] = subject
#        msg['From'] = sender
#        msg['To'] = receiver
#
#        try:
#            smtp_server = ''
#            smtp_port = 587
#            smtp_username = ''
#            smtp_password = ''
#
#            with smtplib.SMTP(smtp_server, smtp_port) as server:
#                server.starttls()
#                server.login(smtp_username, smtp_password)
#                server.send_message(msg)
#
#        except Exception as e:
#            # Gestisci eventuali errori nell'invio della mail
#            print(f"Errore durante l'invio della mail: {e}")

def print_email_falsa(articolo):
    offerta = Offerta.objects.filter(articolo=articolo).order_by('-importo').first()
    if offerta_piu_alta:
        vincitore = offerta_piu_alta.utente
        print(f"Complimenti ad {vincitore.username} per aver vinto l'asta per l'articolo {articolo.titolo}, troverai una mail all'indirizzo {vincitore.email}.")