from django import forms
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

class CreateAnnuncioForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['venditore'].widget = forms.HiddenInput()
        self.fields['venditore'].required = False

class AnnuncioForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__'