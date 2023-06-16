from django import forms
from gestione.models import *

class UtenteForm(forms.ModelForm):

    email = forms.EmailField(max_length=20, required=True)
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    is_venditore = forms.BooleanField(required=False)
    
    class Meta:
        model = Utente
        fields = ["email", "username", "password", "is_venditore"]

class LoginForm(forms.Form):
    username = forms.CharField(label='', 
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'username',
            }
        ))
    password = forms.CharField(label='', 
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'password'
            }
        ))
    