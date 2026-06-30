from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Jugador

class RegistroJugadorForm(UserCreationForm):
    """ Formulario Pro para registrar usuarios con billetera automática """
    class Meta:
        model = Jugador
        fields = ('username', 'email')

class LoginJugadorForm(AuthenticationForm):
    """ Formulario para inicio de sesión seguro """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))