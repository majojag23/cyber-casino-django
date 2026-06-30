from django.db import models
from django.contrib.auth.models import AbstractUser

class Jugador(AbstractUser):
    """ 
    Extendemos el usuario por defecto de Django para añadirle 
    una billetera segura y el control del modo bonus.
    """
    creditos = models.DecimalField(max_digits=12, decimal_places=2, default=500.00)
    es_vip = models.BooleanField(default=False)
    giros_gratis_bonus = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} - Balance: ${self.creditos}"