from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    # Este método ayuda a que en el panel de administrador se vea el nombre real
    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    texto = models.CharField(max_length=200)
    
    # 🔗 RELACIÓN: Vinculamos cada tarea a una Categoría.
    # on_delete=models.CASCADE significa que si borras la categoría "Estudios", todas sus tareas se borran automáticamente.
    # null=True y blank=True permiten que al principio las tareas puedan no tener categoría obligatoria.
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.texto