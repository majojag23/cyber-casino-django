from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Este modelo guardará el dinero real/virtual de cada usuario en el servidor
class PerfilUsuario(models.Model):
    # Aquí cambiamos "User" por la configuración de tu proyecto
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Billetera de {self.usuario.username} - Saldo: ${self.saldo}"

# Obtenemos el modelo de usuario correcto para tu proyecto
Usuario = get_user_model()

# --- MAGIA DE DJANGO ---
@receiver(post_save, sender=Usuario)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.get_or_create(usuario=instance)

@receiver(post_save, sender=Usuario)
def guardar_perfil_usuario(sender, instance, **kwargs):
    # Le preguntamos amablemente a Django si la billetera existe ANTES de guardarla
    if hasattr(instance, 'perfilusuario'):
        instance.perfilusuario.save()