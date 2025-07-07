"""interacion entre la web, la bd con el usuario guarde sus cosas."""
from django import forms
from .models import ModeloCNN
#como interactua el usuario con el vaina web y del vaina web a la base de datos
class ModeloCNNForm(forms.ModelForm):
    """Vista que muestra una lista de modelos CNN registrados en la base de datos."""
    class Meta:
        """Vista para crear y registrar un nuevo modelo CNN."""
        model = ModeloCNN
        fields = ['nombre', 'accuracy', 'descripcion']

class LLMChatForm(forms.Form):
    question = forms.CharField(
        label="Pregunta",
        widget=forms.TextInput(attrs={
            "placeholder": "Escribe tu pregunta...",
            "class": "form-control"
        }),
        required=True
    )
