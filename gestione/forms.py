from django import forms
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
import string

class AnnuncioCreateForm(forms.ModelForm):
    """
    Form usato per la creazione di un annuncio per inserire un :model:'gestione/Articolo'
    """
    class Meta:
        model = Articolo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Sovrascrittura della funzione __init__ che viene utilizzata per riscrivere le label
        dei campi da inserire e nasconde alcune field che l'utente non deve modificare.
        """
        super().__init__(*args, **kwargs)
        self.fields['titolo'].label = "Titolo:"
        self.fields['schedaTecnica'].label = "Scheda tecnica:"
        self.fields['categoria'].label = "Categoria:"
        self.fields['immagine'].label = "Immagine:"
        self.fields['prezzoIniziale'].label = "Prezzo iniziale:"
        self.fields['durataAsta'].label = "Durata asta:"
        self.fields['dataFineAsta'].required = False
        self.fields['dataFineAsta'].widget = forms.HiddenInput()
        self.fields['terminato'].required = False
        self.fields['terminato'].widget = forms.HiddenInput()
        self.fields['venditore'].widget = forms.HiddenInput()
        self.fields['venditore'].required = False
    
    def clean_titolo(self):
        """
        Funzione che controlla che nel titolo non vengano inseriti caratteri speciali.
        """
        titolo = self.cleaned_data.get('titolo')
        # Effettua la validazione per evitare caratteri speciali
        for i in titolo:
            if i in string.punctuation:
                raise forms.ValidationError("Il titolo non può contenere caratteri speciali.")
        return titolo

    def clean_schedaTecnica(self):
        """
        Funzione che controlla che nella schede tecnica non vengano inseriti caratteri speciali.
        """
        schedaTecnica = self.cleaned_data.get('schedaTecnica')
        # Effettua la validazione per evitare caratteri speciali
        for i in schedaTecnica:
            if i in string.punctuation:
                raise forms.ValidationError("La scheda tecnica non può contenere caratteri speciali.")
        return schedaTecnica

class AnnuncioUpdateForm(forms.ModelForm):
    """
    Form usato per la modifica di alcuni campi di un annuncio e permette di modificare
    solo alcuni campi del :model:'gestione/Articolo'.
    """
    class Meta:
        model = Articolo
        fields = ('titolo', 'schedaTecnica', 'categoria')

    def __init__(self, *args, **kwargs):
        """
        Sovrascrittura della funzione __init__ che viene utilizzata per riscrivere le label
        dei campi da modificare.
        """
        super().__init__(*args, **kwargs)
        self.fields['titolo'].label = "Titolo:"
        self.fields['schedaTecnica'].label = "Scheda tecnica:"
        self.fields['categoria'].label = "Categoria:"

# Form riguardanti le offerte
class OffertaCreateForm(forms.Form):
    """
    Form usato per l'inserimento di una nuova offerta del modello :model:'gestione/Offerta'.
    """
    saldo = forms.DecimalField(label='Saldo:', max_digits=7, decimal_places=2, min_value=1)

# Form riguardanti le recensioni
class RecensioneCreateForm(forms.ModelForm):
    """
    Form usato per la creazione di una nuova recensione tramite il modello :model:'gestione/Recensione'.
    """
    class Meta:
        model = Recensione
        fields = ('testo', 'voto')

    def __init__(self, *args, **kwargs):
        """
        Sovrascrittura della funzione __init__ che viene utilizzata per riscrivere le label
        dei campi da modificare.
        """
        super().__init__(*args, **kwargs)
        self.fields['testo'].label = "Commento:"
        self.fields['voto'].label = "Voto:"

    def clean_testo(self):
        """
        Funzione che controlla che nel testo non vengano inseriti caratteri speciali.
        """
        testo = self.cleaned_data.get('testo')
        # Effettua la validazione per evitare caratteri speciali
        for i in testo:
            if i in string.punctuation:
                raise forms.ValidationError("Il testo non può contenere caratteri speciali.")
        return testo
