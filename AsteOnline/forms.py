from django import forms
from gestione.models import *

class VenditoreForm(forms.ModelForm):

    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    via = forms.CharField(max_length=50, required=True)
    numCivico = forms.CharField(max_length=5, required=True)
    CAP = forms.IntegerField(required=True)
    
    class Meta:
        model = Venditore
        fields = ["username", "email", "password", "via", "numCivico", "CAP"]
    
class AcquirenteForm(forms.ModelForm):

    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    via = forms.CharField(max_length=50, required=True)
    numCivico = forms.CharField(max_length=5, required=True)
    CAP = forms.IntegerField(required=True)
    
    class Meta:
        model = Acquirente
        fields = ["username", "email", "password", "via", "numCivico", "CAP"]