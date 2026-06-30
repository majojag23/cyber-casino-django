from django.contrib import admin
from .models import PerfilUsuario

# Esto le dice a Django: "¡Muestra las billeteras en el panel de control!"
admin.site.register(PerfilUsuario)