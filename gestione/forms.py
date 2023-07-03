from django import forms
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
import string

# Form riguardanti gli annunci
class AnnuncioCreateForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dataFineAsta'].required = False
        self.fields['dataFineAsta'].widget = forms.HiddenInput()
        self.fields['terminato'].required = False
        self.fields['terminato'].widget = forms.HiddenInput()
        self.fields['venditore'].widget = forms.HiddenInput()
        self.fields['venditore'].required = False
    
    def clean_titolo(self):
        titolo = self.cleaned_data.get('titolo')
        # Effettua la validazione per evitare caratteri speciali
        for i in titolo:
            if i in string.punctuation:
                raise forms.ValidationError("Il titolo non può contenere caratteri speciali.")
        return titolo

    def clean_schedaTecnica(self):
        schedaTecnica = self.cleaned_data.get('schedaTecnica')
        # Effettua la validazione per evitare caratteri speciali
        for i in schedaTecnica:
            if i in string.punctuation:
                raise forms.ValidationError("Il titolo non può contenere caratteri speciali.")
        return schedaTecnica

class AnnuncioUpdateForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__'

# Form riguardanti le offerte
class OffertaCreateForm(forms.Form):
    saldo = forms.DecimalField(label='Saldo', max_digits=5, decimal_places=2)

# Form riguardanti le recensioni
class RecensioneCreateForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ('testo', 'voto')
