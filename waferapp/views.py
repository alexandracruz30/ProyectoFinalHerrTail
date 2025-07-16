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
from tensorflow.keras.models import load_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import HistorialPrediccion



# Define la ruta
MODEL_PATH = os.path.join(settings.BASE_DIR, 'modelos', 'mi_modelo.h5')
class_labels = [
    "Center", "Donut", "Edge-Loc", "Edge-Ring", "Loc",
    "Near-full", "Random", "Scratch", "None"
]

class DashboardView(TemplateView):
    template_name = "dash/dash.html"  

class procesoModeloView(TemplateView):
    """Vista que muestra la plantilla para el entrenamiento del modelo."""
    template_name = "modelos/procesoModelo.html"  


# Crea una vista simple para home
class HomeView(TemplateView):
    template_name = "base/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos de modelos predefinidos
        context['modelos'] = [
            {
                'nombre': 'InceptionV3',
                'descripcion': 'Modelo Inception V3 optimizado para detectar defectos en obleas de silicio utilizando módulos de inicio que aplican filtros de diferentes tamaños para capturar características a múltiples escalas.',
                'accuracy': '96.4%'
            },
            {
                'nombre': 'ResNet50',
                'descripcion': 'Modelo ResNet entrenado para detectar defectos en obleas de silicio con alta precisión, utilizando conexiones residuales para un aprendizaje más profundo.',
                'accuracy': '98.7%'
            },
            {
                'nombre': 'VGG16',
                'descripcion': 'Modelo VGG entrenado para inspección visual de defectos, basado en convoluciones profundas y simples con excelente capacidad de generalización.',
                'accuracy': '95.2%'
            },
            {
                'nombre': 'MobileNet',
                'descripcion': 'Modelo ligero MobileNet optimizado para procesamiento rápido de imágenes de obleas, ideal para aplicaciones en tiempo real.',
                'accuracy': '94.1%'
            }
        ]
        
        # Información adicional del contexto
        context['total_modelos'] = len(context['modelos'])
        context['modelo_destacado'] = max(context['modelos'], key=lambda x: float(x['accuracy'].rstrip('%')))
        
        return context

class SignUpView(FormView):
    """Vista para el registro de nuevos usuarios utilizando el formulario por defecto de Django."""
    template_name = 'usuario/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('modelos:home')  

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(None, "Por favor, corrige los errores e intenta nuevamente.")
        return super().form_invalid(form)

class UserLoginView(LoginView):
    """Vista para iniciar sesión de usuario autenticado."""
    template_name = 'usuario/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('modelos:home')  

    def get_success_url(self):
        return str(self.success_url)

    def form_invalid(self, form):
        form.add_error(None, "Usuario o contraseña incorrectos. Intenta de nuevo.")
        return super().form_invalid(form)

class UserLogoutView(LogoutView):
    """Vista para cerrar sesión del usuario."""
    next_page = reverse_lazy('modelos:home') 

class EntrenamientoView(TemplateView):
    """Vista que muestra la plantilla para el entrenamiento del modelo."""
    template_name = "modelos/entrena.html"  # ✅ Corregido (era "modelos/modelos/entrena.html")

class DetallesUsoView(TemplateView):
    """Vista que muestra detalles del uso del modelo CNN."""
    template_name = "modelos/detalles.html"  # ✅ Corregido (era "modelos/modelos/detalles.html")

class GaleriaView(TemplateView):
    """Vista para mostrar la galería de imágenes."""
    template_name = "modelos/galeria.html"

class ModeloCreateView(TemplateView):
    """Vista para crear y registrar un nuevo modelo CNN."""
    template_name = "modelos/add_modelo.html"

class PruebasView(TemplateView):
    """Vista para realizar pruebas con el modelo CNN entrenado."""
    template_name = 'pruebas/pruebas.html'  # ✅ Corregido (era 'modelos/pruebas/pruebas.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_labels'] = class_labels
        return context
    
    def post(self, request):
        resultado = None
        probabilities = None
        error = None
        image_preview = None

        try:
            # Cargar el modelo solo cuando se necesite
            if not os.path.exists(MODEL_PATH):
                error = f"El modelo no existe en la ruta: {MODEL_PATH}"
                raise FileNotFoundError(error)
            
            model = load_model(MODEL_PATH)  # Cargar aquí
            
            file = request.FILES.get('uploaded_image')
            if not file:
                error = "No se seleccionó ninguna imagen."
            else:
                img = Image.open(file).convert('RGB')
                img = img.resize((26, 26))
                img_arr = np.array(img).astype('float32') / 255.0
                x = np.expand_dims(img_arr, axis=0)

                prediction = model.predict(x)
                predicted_class_idx = np.argmax(prediction)
                resultado = class_labels[predicted_class_idx]
                probabilities = {label: float(prob) for label, prob in zip(class_labels, prediction[0])}

                buffered = BytesIO()  # Corregido el typo
                img.save(buffered, format="PNG")
                image_preview = base64.b64encode(buffered.getvalue()).decode()
                
        except Exception as e:
            error = f"Error al procesar la imagen: {str(e)}"

        context = {
            'resultado': resultado,
            'probabilities': probabilities,
            'class_labels': class_labels,
            'error': error,
            'image_preview': image_preview,
        }
        return render(request, self.template_name, context)
    
class HistorialView(LoginRequiredMixin, ListView):
        model = HistorialPrediccion
        template_name = 'pruebas/historial.html'
        context_object_name = 'historial'

        def get_queryset(self):
        # Solo muestra el historial del usuario autenticado, ordenado por fecha descendente
            return HistorialPrediccion.objects.filter(usuario=self.request.user).order_by('-fecha')


