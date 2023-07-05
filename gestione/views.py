from .models import *
from .forms import *

from django.contrib import messages
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

# Costanti
CATEGORIE = ['Elettronica', 'Informatica', 'CD e Vinili', 'Videogiochi', 'Strumenti musicali', 'Film e DVD']

# View legate agli Annunci
class AnnuncioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    CreateView usata per creare un nuovo annuncio e utilizza come modello :model:'gestione.Articolo'.

    **Template:**
    :template:'gestione/annuncio_create.html'
    """
    model = Articolo
    title = "Inserimento annuncio"
    form_class = AnnuncioCreateForm
    template_name = 'annuncio_create.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        """
        Questa funzione è ereditata da UserPassesTestMixin che obbliga la View a 
        controllare che l'utente faccia parte del gruppo dei Venditori.
        """
        return self.request.user.groups.filter(name='Venditori').exists()

    def form_valid(self, form):
        """
        Questa funzione che viene eseguita se il form inserito è valido e sovrascrive
        il campo venditore con l'username dell'utente.
        """
        form.instance.venditore = self.request.user.username
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Questa funzione viene eseguita su il form non è corretta e viene ricaricata 
        con gli errori.
        """
        return render(self.request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Questa funzione viene effettuata con il metodo POST e FILE per permettere il 
        caricamento dell'immagine e controlla se il form è valido e poi in base a questo
        carica la giusta funzione.
        """
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.venditore = self.request.user.username
            messages.success(request, "Annuncio inserito con successo.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AnnuncioDetailView(DetailView):
    """
    DetailView che fa vedere l'articolo e tutti i suoi dettagli legati all'asta,
    il modello è sempre :model:'gestione/Articolo'.

    **Template:**
    :template:'gestione/annuncio_detail.html'
    """
    model = Articolo
    template_name = 'annuncio_detail.html'
    context_object_name = 'articolo'

    def get_context_data(self, **kwargs):
        """
        Funzione che carica nel context i vari dati che servono al template: l'ultima offerta,
        il tempo rimanente, lo username e gli articoli consigliati.
        """
        context = super().get_context_data(**kwargs)
        articolo = self.object 

        # Ottieni l'ultima offerta per l'articolo
        ultima_offerta = Offerta.objects.filter(articolo=self.object).order_by('-id').first()
        
        # Viene ottenuto il tempo rimanente
        if str(articolo.dataFineAsta - timezone.now())[0] == '-':
            context['tempo_restante'] = 0
            articolo.terminato = True
            articolo.save()
        else:
            context['tempo_restante'] = round((articolo.dataFineAsta - timezone.now()).seconds / 60)
        context['ultima_offerta'] = ultima_offerta
        context['username'] = self.request.user.username

        # Vengono ottenuti gli articoli consigliati
        articoli_consigliati = Articolo.objects.filter(
            Q(titolo__icontains=articolo.titolo) | Q(categoria=articolo.categoria, prezzoIniziale__range=[articolo.prezzoIniziale-20, articolo.prezzoIniziale+20])
        ).exclude(id=articolo.id)[:3]
        context['articoli_consigliati'] = articoli_consigliati

        if (self.request.user.groups.filter(name='Venditori').exists()):
            context['is_venditore'] = True
        else:
            context['is_venditore'] = False
        
        return context

class AnnuncioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    UpdateView che permette di aggiornare dei dettagli legati all'asta,
    il modello è sempre :model:'gestione/Articolo'.

    **Template:**
    :template:'gestione/annuncio_update.html'
    """
    model = Articolo
    form_class = AnnuncioUpdateForm
    template_name = 'annuncio_update.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        """
        Funzione che controlla che l'utente che vuole modificare l'asta sia il venditore
        creatore dell'asta stessa.
        """
        articolo = self.get_object()
        return articolo.venditore == self.request.user.username

    def form_valid(self, form):
        """
        Funzione che controlla che il form sia valido e poi inserisce il messaggio dell'aggiornamento riuscito.
        """
        response = super().form_valid(form)

        messages.success(self.request, "Annuncio aggiornato correttamente.")

        return response


class AnnuncioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DeleteView che permette di eliminare un annuncio, il modello è 
    sempre :model:'gestione/Articolo'.

    **Template:**
    :template:'gestione/annuncio_delete.html'
    """
    model = Articolo
    template_name = 'annuncio_delete.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        """
        Funzione che controlla che l'utente che vuole eliminare l'asta sia il venditore
        creatore dell'asta stessa.
        """
        articolo = self.get_object()
        return articolo.venditore == self.request.user.username

class AnnuncioSearchView(ListView):
    """
    ListView che permette di cercare tutti gli articoli che hanno nel titolo la parola
    che viene ricercata, il modello è sempre :model:'gestione/Articolo'.

    **Template:**
    :template:'gestione/annuncio_search.html'
    """
    model = Articolo
    template_name = 'annuncio_search.html'
    context_object_name = 'articoli'

    def get_queryset(self):
        """
        Funzione, ereditata da ListView, che viene utilizzata per ottenere la queryset.
        """
        query = self.request.GET.get('q')  # Ottiene il valore della query dalla richiesta GET
        if query:
            return Articolo.objects.filter(titolo__icontains=query)  # Filtra gli articoli per il titolo che contiene la query
        else:
            return Articolo.objects.all()  # Restituisce tutti gli articoli se la query non è presente

    def get_context_data(self, **kwargs):
        """
        Funzione che carica nel context i vari dati che servono al template e cioè il risultato
        delle query.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')  # Passa il valore della query al contesto del template
        return context

# View riguardanti le offerte
class OffertaCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View che viene utilizzata per fare un'offerta ad un'asta, il modello utilizzato
    è :model:'gestione/Offerta'

    **Template:**
    :template:'gestione/offerta_create.html'
    """
    def test_func(self):
        """
        Questa funzione è ereditata da UserPassesTestMixin che obbliga la View a 
        controllare che l'utente faccia parte del gruppo dei Acquirenti.
        """
        return self.request.user.groups.filter(name='Acquirenti').exists()

    def get(self, request, articolo_id):
        """
        Questa funzione è stata inserita in quanto senza di essa non so perché non funziona
        la View.
        """
        articolo = get_object_or_404(Articolo, pk=articolo_id)
        form = OffertaCreateForm()
        return render(request, 'offerta_create.html', {'form': form, 'articolo': articolo})

    def post(self, request, articolo_id):
        """
        Questa funzione viene utilizzata per il metodo POST, controlla che l'articolo esista,
        che il form sia valido e che l'offerta sia più alta dell'ultima inserita e poi la salva
        reindirizzando poi l'utente sulla pagina detail dell'annuncio.
        """
        articolo = get_object_or_404(Articolo, pk=articolo_id)
        form = OffertaCreateForm(request.POST)

        if form.is_valid():
            saldo = form.cleaned_data['saldo']
            if saldo < articolo.prezzoIniziale:
                form.add_error('saldo', 'L\'offerta deve essere maggiore dell\'offerta iniziale.')
            elif articolo.offerta_set.filter(saldo__gte=saldo).exists():
                form.add_error('saldo', 'L\'offerta deve essere maggiore di quelle già fatte.')
            else:
                offerta = Offerta(acquirente=request.user, articolo=articolo, saldo=saldo)
                offerta.save()
                messages.success(request, "Offerta inserita con successo.")
                return redirect('gestione:annuncio-detail', pk=articolo.id)

        return render(request, 'offerta_create.html', {'form': form, 'articolo': articolo})

# View riguardanti le recensioni
class RecensioneListView(ListView):
    """
    ListView che mostra le recensini di un dato venditore e anche la lista degli 
    articoli che il venditore ha in vendita, , il modello usato è quello del 
    :model:'gestione/Recensione'

    **Template:**
    :template:'gestione/recensione_list.html'
    """
    model = Recensione
    template_name = 'recensione_list.html'
    context_object_name = 'recensioni'

    def get_context_data(self, **kwargs):
        """
        Funzione che carica nel context i vari dati che servono al template tipo il nome del
        venditore, gli articoli del venditore e il nome del venditore.
        """
        context = super().get_context_data(**kwargs)
        venditore = self.kwargs['venditore_username']
        articoli = Articolo.objects.filter(venditore=venditore)
        context['articoli'] = articoli
        context['venditore'] = venditore

        if (self.request.user.groups.filter(name='Venditori').exists()):
            context['gruppo_venditore'] = True
        else:
            context['gruppo_venditore'] = False

        return context

    def get_queryset(self):
        """
        Funzione, ereditata da ListView, che viene utilizzata per ottenere la queryset.
        """
        venditore = User.objects.get(username=self.kwargs['venditore_username'])
        return Recensione.objects.filter(venditore=venditore)

class RecensioneCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    CreateView viene usata per creare recensioni dei venditori, il modello usato 
    è quello del :model:'gestione/Recensione'

    **Template:**
    :template:'gestione/recensione_create.html'
    """
    model = Recensione
    form_class = RecensioneCreateForm
    template_name = 'recensione_create.html'

    def test_func(self):
        """
        Questa funzione è ereditata da UserPassesTestMixin che obbliga la View a 
        controllare che l'utente faccia parte del gruppo dei Acquirenti.
        """
        return self.request.user.groups.filter(name='Acquirenti').exists()

    def form_valid(self, form):
        """
        Funzione che viene eseguita se il form è valido e inserisce i dati nel campo
        venditore e acquirente.
        """
        venditore = User.objects.get(username=self.kwargs['venditore_username'])
        form.instance.acquirente = self.request.user
        form.instance.venditore = venditore
        messages.success(self.request, "Recensione inserita correttamente.")
        return super().form_valid(form)

    def get_success_url(self):
        """
        Funzione che riscrive dinamicamente la variabile success_url con la pagina recensione-list
        del venditore.
        """
        venditore_username = self.kwargs['venditore_username']
        return reverse('gestione:recensione-list', kwargs={'venditore_username': venditore_username})