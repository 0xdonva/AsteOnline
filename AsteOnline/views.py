from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

from .forms import *
from gestione.models import *

class AcquirenteCreate(CreateView):
    """
    View che permette la registrazione di un utente come Acquirente.

    **Template:**
    :template:'registration.html'
    """
    form_class = AcquirenteForm
    template_name = 'registration.html'
    success_url = "/login/"

class VenditoreCreate(CreateView):
    """
    View che permette la registrazione di un utente come Venditore.

    **Template:**
    :template:'registration.html'
    """
    form_class = VenditoreForm
    template_name = 'registration.html'
    success_url = "/login/"

class UtenteCreate(TemplateView):
    """
    TemplateView che visualizza una pagina che permette la scelta tra la 
    registrazione come Acquirente o come Venditore.

    **Template:**
    :template:'preregistration.html'
    """
    template_name = 'preregistration.html'

class HomeView(ListView):
    """
    ListView che visualizza homepage in cui vengono visualizzati gli articoli
    presenti nel database in base alla categoria.

    **Template:**
    :template:'home.html'
    """
    model = Articolo
    template_name = 'home.html'
    context_object_name = 'articoli'

    def get_context_data(self, **kwargs):
        """
        Funzione che oltre ai dati legati agli articoli nel database carica
        un booleano che è vero se è un venditore e se lo è inserisce nel context
        anche l'username del venditore, per rendere la navbar dinamica.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            group = Group.objects.get(name='Venditori')
            is_venditore = group in user.groups.all()
            context['is_venditore'] = is_venditore
            if is_venditore:
                context['username'] = self.request.user.username
        return context

class LogoutView(LogoutView):
    """
    LogoutView che viene utilizzata per il logout degli utenti.
    """

    def get(self, request):
        logout(request)

        return redirect('homepage')