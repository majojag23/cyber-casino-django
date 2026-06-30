from django.contrib import admin
from .models import Tarea, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['id', 'texto', 'categoria']
    list_filter = ['categoria']
    search_fields = ['texto']
    list_editable = ['categoria']
    
    # 🚀 ¡Agregamos nuestra acción personalizada a la lista!
    actions = ['marcar_como_importante']

    # Esta función hace la magia en la base de datos
    @admin.action(description='Marcar tareas seleccionadas como [IMPORTANTE]')
    def marcar_como_importante(self, request, queryset):
        # Recorremos cada tarea que seleccionaste en la tabla
        for tarea in queryset:
            if not tarea.texto.startswith("[IMPORTANTE]"):
                tarea.texto = f"[IMPORTANTE] {tarea.texto}"
                tarea.save() # Guarda el cambio directo en la base de datos