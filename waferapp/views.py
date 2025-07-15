"""PARA LO QUE ES ESTA CLASE NO SE LA VERDAD, MENTIRA PARA TODOS LOS 
URLS DEL APP VENGAN A VISITARLA Y MOSTRAR HTML"""
import os
import numpy as np
from PIL import Image
from django import forms
from io import BytesIO
import base64
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from tensorflow.keras.models import load_model
from .models import ModeloCNN
from .forms import ModeloCNNForm, CustomUserCreationForm, CustomAuthenticationForm
from .forms import LLMChatForm
from django import forms


class DashboardView(TemplateView):
    template_name = "modelos/dash/dash.html"

class procesoModeloView(TemplateView):
    """Vista que muestra la plantilla para el entrenamiento del modelo."""
    template_name = "modelos/modelos/procesoModelo.html"

#Galería
class GaleriaView(TemplateView):
    """Vista que muestra fotos y datos importantes del modelo."""
    template_name = "modelos/galeria/galeria.html"

class HomeView(ListView):
    """Vista que muestra una lista de modelos CNN registrados en la base de datos."""
    model = ModeloCNN
    template_name = "modelos/base/index.html"
    context_object_name = "modelos"

class ModeloCreateView(CreateView):
    """Vista para crear y registrar un nuevo modelo CNN."""
    model = ModeloCNN
    form_class = ModeloCNNForm
    template_name = "modelos/modelos/add_modelo.html"
    success_url = reverse_lazy('modelos:home')

class SignUpView(FormView):
    """Vista para el registro de nuevos usuarios utilizando el formulario personalizado."""
    template_name = 'modelos/usuario/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('modelos:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'¡Bienvenido {user.first_name}! Tu cuenta ha sido creada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrige los errores e intenta nuevamente.")
        return super().form_invalid(form)

class UserLoginView(LoginView):
    """Vista para iniciar sesión de usuario autenticado."""
    template_name = 'modelos/usuario/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('modelos:home')

    def get_success_url(self):
        return str(self.success_url)

    def form_valid(self, form):
        messages.success(self.request, f'¡Bienvenido {form.get_user().first_name or form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos. Intenta de nuevo.")
        return super().form_invalid(form)

class UserLogoutView(LogoutView):
    """Vista para cerrar sesión del usuario."""
    next_page = reverse_lazy('modelos:home')

class EntrenamientoView(TemplateView):
    """Vista que muestra la plantilla para el entrenamiento del modelo."""
    template_name = "modelos/modelos/entrena.html"

class DetallesUsoView(TemplateView):
    """Vista que muestra detalles del uso del modelo CNN."""
    template_name = "modelos/modelos/detalles.html"

print("BASE_DIR:", settings.BASE_DIR)
# Carga el modelo una sola vez
MODEL_PATH = os.path.join(settings.BASE_DIR, 'modelos', 'mi_modelo.h5')
model = load_model(MODEL_PATH)

class_labels = [
    "Center", "Donut", "Edge-Loc", "Edge-Ring", "Loc",
    "Near-full", "Random", "Scratch", "None"
]

class PruebasView(TemplateView):
    """Vista para realizar pruebas con el modelo CNN entrenado."""
    template_name = 'modelos/pruebas/pruebas.html'

    def get(self, request):
        return render(request, self.template_name, {'class_labels': class_labels})

    def post(self, request):
        resultado = None
        probabilities = None
        error = None
        image_preview = None

        try:
            file = request.FILES.get('uploaded_image')
            if not file:
                error = "No se seleccionó ninguna imagen."
            else:
                img = Image.open(file).convert('RGB')
                img = img.resize((26, 26))  # Ajusta al input de tu modelo
                img_arr = np.array(img).astype('float32') / 255.0
                x = np.expand_dims(img_arr, axis=0)

                prediction = model.predict(x)
                predicted_class_idx = np.argmax(prediction)
                resultado = class_labels[predicted_class_idx]
                probabilities = {label: float(prob) for label,
                prob in zip(class_labels, prediction[0])}

                buffered = BytesIO()
                img.save(buffered, format="PNG")
                image_preview = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            error = str(e)

        context = {
            'resultado': resultado,
            'probabilities': probabilities,
            'class_labels': class_labels,
            'error': error,
            'image_preview': image_preview,
        }
        return render(request, self.template_name, context)
    
