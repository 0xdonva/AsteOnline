from django import forms
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

# Form riguardanti gli annunci
class AnnuncioCreateForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['immagine'].required = False
        self.fields['venditore'].widget = forms.HiddenInput()
        self.fields['venditore'].required = False

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
