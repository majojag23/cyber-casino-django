from django import forms
from .models import Tarea

# 1. Formulario basado en Modelo
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['texto']
        widgets = {
            'texto': forms.TextInput(attrs={
                'id': 'input-nueva-tarea-form',
                'placeholder': 'Escribe una tarea para validar...',
                'style': 'flex-grow: 1; padding: 12px; background: #121214; border: 1px solid #29292e; border-radius: 6px; color: white;'
            })
        }

    def clean_texto(self):
        texto = self.cleaned_data.get('texto')
        if "prohibido" in texto.lower():
            raise forms.ValidationError("¡Lo siento Mariana! No puedes usar palabras prohibidas en tus tareas. ❌")
        if len(texto) < 5:
            raise forms.ValidationError("La tarea es demasiado corta. Debe tener al menos 5 caracteres. ⚠️")
        return texto


# 2. Formulario Estándar (¡Revisa bien este nombre!)
class PlanEstudioForm(forms.Form):
    nombre_estudiante = forms.CharField(
        max_length=100,
        label="Tu Nombre",
        widget=forms.TextInput(attrs={
            'placeholder': '¿Quién va a estudiar hoy, Mariana?',
            'style': 'width: 100%; padding: 12px; background: #121214; border: 1px solid #29292e; border-radius: 6px; color: white; margin-bottom: 15px;'
        })
    )
    horas_por_dia = forms.IntegerField(
        label="Horas por día",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ej. 2',
            'style': 'width: 100%; padding: 12px; background: #121214; border: 1px solid #29292e; border-radius: 6px; color: white; margin-bottom: 15px;'
        })
    )
    dias_por_semana = forms.IntegerField(
        label="Días a la semana",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ej. 5',
            'style': 'width: 100%; padding: 12px; background: #121214; border: 1px solid #29292e; border-radius: 6px; color: white; margin-bottom: 15px;'
        })
    )

    def clean_dias_por_semana(self):
        dias = self.cleaned_data.get('dias_por_semana')
        if dias < 1 or dias > 7:
            raise forms.ValidationError("¡Imposible! Una semana solo tiene entre 1 y 7 días. 📅")
        return dias

    def clean_horas_por_dia(self):
        horas = self.cleaned_data.get('horas_por_dia')
        if horas < 1 or horas > 24:
            raise forms.ValidationError("Un día solo tiene 24 horas. ¡No olvides dormir! 😴")
        return horas