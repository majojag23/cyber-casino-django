from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Obtenemos tu modelo de usuario personalizado (usuarios.Jugador)
Usuario = get_user_model()

class FormularioRegistroVIP(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields