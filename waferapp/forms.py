"""interacion entre la web, la bd con el usuario guarde sus cosas."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
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

class CustomUserCreationForm(UserCreationForm):
    """Formulario personalizado de registro de usuario"""
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )
    first_name = forms.CharField(
        label="Nombre",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        label="Apellido",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu apellido'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['username'].widget.attrs.update({'placeholder': 'usuario123'})
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mínimo 8 caracteres'})
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repite tu contraseña'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Formulario personalizado de autenticación"""
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre de usuario'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Tu contraseña'
        })
    )
