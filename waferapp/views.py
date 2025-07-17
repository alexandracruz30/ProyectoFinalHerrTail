"""PARA LO QUE ES ESTA CLASE NO SE LA VERDAD, MENTIRA PARA TODOS LOS 
URLS DEL APP VENGAN A VISITARLA Y MOSTRAR HTML"""
import os
import base64
from io import BytesIO

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

from django import forms
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import FormView

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ModeloCNN, ImagenSubida
from .forms import ModeloCNNForm, LLMChatForm

import sys
import os
sys.path.append(os.path.join(settings.BASE_DIR, 'llmDocs'))
sys.path.append(r'c:\cnnFinalPry\cnnFinalPry\llmDocs')


# ✅ CONFIGURACIÓN CORRECTA DEL MODELO CNN
MODEL_PATH = os.path.join(settings.BASE_DIR, 'waferapp', 'mi_modelo.h5')

# Verificar si el archivo existe antes de cargarlo
if os.path.exists(MODEL_PATH):
    try:
        cnn_model = load_model(MODEL_PATH)
        print(f"✅ Modelo cargado exitosamente desde: {MODEL_PATH}")
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        cnn_model = None
else:
    print(f"❌ No se encontró el archivo del modelo en: {MODEL_PATH}")
    cnn_model = None

class_labels = [
    "Center", "Donut", "Edge-Loc", "Edge-Ring", "Loc",
    "Near-full", "Random", "Scratch", "None"
]

class DashboardView(TemplateView):
    template_name = "dash/dash.html"  # ✅ Corregido

class procesoModeloView(TemplateView):
    """Vista que muestra la plantilla para el entrenamiento del modelo."""
    template_name = "modelos/procesoModelo.html"  # ✅ Corregido

# Comenta estas vistas temporalmente
# class HomeView(ListView):
#     """Vista que muestra una lista de modelos CNN registrados en la base de datos."""
#     model = ModeloCNN
#     template_name = "base/index.html"  # ✅ Corregido
#     context_object_name = "modelos"

# class ModeloCreateView(CreateView):
#     """Vista para crear y registrar un nuevo modelo CNN."""
#     model = ModeloCNN
#     form_class = ModeloCNNForm
#     template_name = "modelos/modelos/add_modelo.html"
#     success_url = reverse_lazy('modelos:home')

# Crea una vista simple para home temporalmente
class HomeView(TemplateView):
    template_name = "base/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos de modelos predefinidos con información más completa
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
        ]
        
        # Información adicional del contexto
        context['total_modelos'] = len(context['modelos'])
        context['modelo_destacado'] = max(context['modelos'], key=lambda x: float(x['accuracy'].rstrip('%')))
        
        return context

class SignUpView(FormView):
    """Vista para el registro de nuevos usuarios utilizando el formulario por defecto de Django."""
    template_name = 'usuario/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('modelos:home')  # ✅ Cambiado

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
    success_url = reverse_lazy('modelos:home')  # ✅ Cambiado

    def get_success_url(self):
        return str(self.success_url)

    def form_invalid(self, form):
        form.add_error(None, "Usuario o contraseña incorrectos. Intenta de nuevo.")
        return super().form_invalid(form)

class llmView(TemplateView):
    template_name = "modelos/llm/llm.html"
    form_class = LLMChatForm

class UserLogoutView(LogoutView):
    """Vista para cerrar sesión del usuario."""
    next_page = reverse_lazy('modelos:home')  # ✅ Cambiado

class EntrenamientoView(TemplateView):
    """Vista que muestra la plantilla para el entrenamiento del modelo."""
    template_name = "modelos/entrena.html"  # ✅ Corregido (era "modelos/modelos/entrena.html")

class DetallesUsoView(TemplateView):
    """Vista que muestra detalles del uso del modelo CNN."""
    template_name = "modelos/detalles.html"  # ✅ Corregido (era "modelos/modelos/detalles.html")

class GaleriaView(TemplateView):
    """Vista para mostrar la galería de imágenes."""
    template_name = "modelos/galeria.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lista de imágenes para el carrusel de datos
        context['datos_imgs'] = [
            {'src': 'galeria/datos/1.png', 'alt': 'Dato 1', 'title': 'Imagen 1', 'desc': 'Descripción de la imagen 1'},
            {'src': 'galeria/datos/2.png', 'alt': 'Dato 2', 'title': 'Imagen 2', 'desc': 'Descripción de la imagen 2'},
            {'src': 'galeria/datos/3.png', 'alt': 'Dato 3', 'title': 'Imagen 3', 'desc': 'Descripción de la imagen 3'},
            {'src': 'galeria/datos/4.png', 'alt': 'Dato 4', 'title': 'Imagen 4', 'desc': 'Descripción de la imagen 4'},
            {'src': 'galeria/datos/5.png', 'alt': 'Dato 5', 'title': 'Imagen 5', 'desc': 'Descripción de la imagen 5'},
            {'src': 'galeria/datos/6.png', 'alt': 'Dato 6', 'title': 'Imagen 6', 'desc': 'Descripción de la imagen 6'},
            {'src': 'galeria/datos/7.png', 'alt': 'Dato 7', 'title': 'Imagen 7', 'desc': 'Descripción de la imagen 7'},
        ]
        # Lista de imágenes para el carrusel de obleas
        context['obleas_imgs'] = [
            {'src': 'galeria/obleas/8.png', 'alt': 'Oblea 8', 'title': 'Oblea 8', 'desc': 'Descripción de la oblea 8'},
            {'src': 'galeria/obleas/9.png', 'alt': 'Oblea 9', 'title': 'Oblea 9', 'desc': 'Descripción de la oblea 9'},
            {'src': 'galeria/obleas/10.png', 'alt': 'Oblea 10', 'title': 'Oblea 10', 'desc': 'Descripción de la oblea 10'},
            {'src': 'galeria/obleas/11.png', 'alt': 'Oblea 11', 'title': 'Oblea 11', 'desc': 'Descripción de la oblea 11'},
        ]
        return context

class ModeloCreateView(TemplateView):
    """Vista para crear y registrar un nuevo modelo CNN."""
    template_name = "modelos/add_modelo.html"
    success_url = reverse_lazy('modelos:home')  # ✅ Cambiado


class PruebasView(LoginRequiredMixin, TemplateView):
    """Vista para realizar pruebas con el modelo CNN entrenado y guardar el historial de imágenes."""
    template_name = 'pruebas/pruebas.html'

    def get(self, request):
        # Trae historial de imágenes del usuario
        historial = ImagenSubida.objects.filter(usuario=request.user).order_by('-fecha_subida')[:10]
        return render(request, self.template_name, {'class_labels': class_labels, 'historial': historial})

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

                prediction = cnn_model.predict(x)
                predicted_class_idx = np.argmax(prediction)
                resultado = class_labels[predicted_class_idx]
                probabilities = {label: float(prob) for label, prob in zip(class_labels, prediction[0])}

                # Guarda la imagen en el historial del usuario
                imagen_obj = ImagenSubida.objects.create(
                    usuario=request.user,
                    imagen=file,
                    resultado=resultado
                )
                image_preview = imagen_obj.imagen.url  # Para mostrar la imagen guardada (MEDIA_URL configurado)
        except Exception as e:
            error = str(e)

        # Trae historial actualizado
        historial = ImagenSubida.objects.filter(usuario=request.user).order_by('-fecha_subida')[:10]

        context = {
            'resultado': resultado,
            'probabilities': probabilities,
            'class_labels': class_labels,
            'error': error,
            'image_preview': image_preview,
            'historial': historial,
        }
        return render(request, self.template_name, context)

# ✅ CONFIGURACIÓN CORRECTA PARA llmDocs
# ...existing code...

# ✅ CONFIGURACIÓN CORRECTA PARA llmDocs
import sys
import os
# Cambia esta línea:
sys.path.append(os.path.join('C:', 'cnnFinalPry', 'cnnFinalPry'))

# Imports para llmDocs
from llmDocs.main import consultar_llm
from .utils import consultar_llm as consultar_llm_local
from llmDocs.utils import buscar_contexto, armar_prompt

# ...existing code...
# Carga del modelo CNN
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# El modelo ya está cargado arriba, no necesitamos cargarlo de nuevo
clases = ["Center", "Donut", "Edge-Loc", "Edge-Ring", "Loc", "Near-full", "Random", "Scratch", "none"]

@csrf_exempt
def procesar_imagen(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image_path = default_storage.save('uploads/' + image_file.name, image_file)
        image_url = default_storage.url(image_path)

        # Preprocesar la imagen según lo que espera tu CNN
        img = Image.open(image_file).convert('RGB').resize((26, 26))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predicción
        pred = cnn_model.predict(img_array)
        clase_idx = int(np.argmax(pred))
        etiqueta = clases[clase_idx]

        # Buscar contexto usando la etiqueta
        try:
            from .utils import buscar_contexto, armar_prompt, consultar_llm
            contexto = buscar_contexto(etiqueta, top_k=1)
            print("Contexto encontrado:", contexto)
            prompt = armar_prompt(contexto, f"El defecto es '{etiqueta}'. ¿Qué significa este defecto y qué acciones se recomiendan?")
            respuesta_llm = consultar_llm(prompt)
        except Exception as e:
            print(f"Error con LLM: {e}")
            respuesta_llm = f"Defecto detectado: {etiqueta}"

        return JsonResponse({
            "image_url": image_url,
            "respuesta": f"🟢 Clasificación: <b>{etiqueta}</b><br>{respuesta_llm}"
        })
    return JsonResponse({"error": "No se envió una imagen."}, status=400)


import markdown
from django.utils.safestring import mark_safe

class LLMDesdeModelosView(FormView):
    template_name = "llm/llm.html"
    form_class = LLMChatForm
    success_url = reverse_lazy("modelos:llm/llm")

    def form_valid(self, form):
        question = form.cleaned_data["question"]
        try:
            respuesta = consultar_llm(question)
        except Exception as e:
            respuesta = f"Error al consultar el LLM: {e}"
        # Devuelve un formulario vacío para limpiar el campo
        form = self.form_class()
        return self.render_to_response(self.get_context_data(
            form=form,
            user_question=question,
            respuesta=respuesta
        ))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chat_history"] = [
            {"sender": "user", "text": "¿Cuál es la capital de Francia?"},
            {"sender": "llm", "text": "La capital de Francia es París."},
        ]
        if "user_question" in kwargs:
            context["user_question"] = kwargs["user_question"]
        if "respuesta" in kwargs:
            context["respuesta"] = kwargs["respuesta"]
        return context

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os
from django.conf import settings
from pydub import AudioSegment

# Importar funciones de utils.py local para audio
from .utils import normalizar_audio, limpiar_audio, transcribir_whisper, texto_a_audio

@method_decorator(csrf_exempt, name='dispatch')
class ProcesarAudioView(View):
    def post(self, request):
        audio_file = request.FILES.get('audio')
        ruido_segundos = int(request.POST.get('ruido_segundos', 1))

        if not audio_file:
            return JsonResponse({'error': 'No se recibió archivo de audio'}, status=400)

        # Guarda el archivo recibido
        audio_dir = os.path.join(settings.MEDIA_ROOT, "audios")
        os.makedirs(audio_dir, exist_ok=True)
        
        # Verificar el tamaño del archivo
        if audio_file.size == 0:
            return JsonResponse({'error': 'El archivo de audio está vacío'}, status=400)
        
        # Usar extensión .wav directamente
        input_raw = os.path.join(audio_dir, 'input_raw.wav')
        
        try:
            with open(input_raw, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            
            # Verificar que el archivo se guardó correctamente
            if not os.path.exists(input_raw) or os.path.getsize(input_raw) == 0:
                return JsonResponse({'error': 'Error al guardar el archivo de audio'}, status=500)
            
        except Exception as e:
            return JsonResponse({'error': f'Error al guardar audio: {e}'}, status=500)

        # Convierte a WAV con formato estándar
        input_wav = os.path.join(audio_dir, 'input.wav')
        try:
            # Cargar el audio usando pydub
            audio = AudioSegment.from_file(input_raw)
            
            # Convertir a formato estándar: 16kHz, mono, 16-bit
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            
            # Exportar como WAV
            audio.export(input_wav, format='wav')
            
        except Exception as e:
            return JsonResponse({'error': f'Error al convertir audio: {e}. Intenta grabar de nuevo.'}, status=500)

        # Procesamiento con las funciones de utils
        try:
            wav_norm = os.path.join(audio_dir, "input_norm.wav")
            wav_limpio = os.path.join(audio_dir, "input_limpio.wav")
            
            normalizar_audio(input_wav, wav_norm)
            limpiar_audio(wav_norm, wav_limpio, noise_clip_seconds=ruido_segundos)
            
            pregunta = transcribir_whisper(wav_limpio)
            if not pregunta.strip():
                return JsonResponse({'error': 'No se detectó voz en el audio. Intenta hablar más claro.'})
            
            # Usar la función local de consultar_llm
            from .utils import consultar_llm
            respuesta = consultar_llm(pregunta)
            
            audio_respuesta = os.path.join(audio_dir, "respuesta_llm.wav")
            texto_a_audio(respuesta, audio_respuesta)

            audio_url = settings.MEDIA_URL + "audios/respuesta_llm.wav"
            return JsonResponse({
                'pregunta': pregunta,
                'respuesta': respuesta,
                'audio_url': audio_url,
            })
            
        except Exception as e:
            return JsonResponse({'error': f'Error procesando audio: {e}'}, status=500)
    
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

@csrf_exempt
def api_llm_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "")
            respuesta = consultar_llm_local(question)
            return JsonResponse({"respuesta": respuesta})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)