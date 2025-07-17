# ==============================================================================
# IMPORTS DEL SISTEMA Y LIBRERÍAS ESTÁNDAR
# ==============================================================================
import os
import sys
import json
import base64
from io import BytesIO

# ==============================================================================
# IMPORTS DE TERCEROS
# ==============================================================================
import numpy as np
import markdown
from PIL import Image
from pydub import AudioSegment

# TensorFlow/Keras
from tensorflow.keras.models import load_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import HistorialPrediccion

# ==============================================================================
# IMPORTS DE DJANGO
# ==============================================================================
from django import forms
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import FormView

# ==============================================================================
# IMPORTS DE DJANGO REST FRAMEWORK
# ==============================================================================
from rest_framework.decorators import api_view
from rest_framework.response import Response

# ==============================================================================
# IMPORTS LOCALES DE LA APLICACIÓN
# ==============================================================================
from .models import ModeloCNN, ImagenSubida
from .forms import ModeloCNNForm, LLMChatForm

# ==============================================================================
# CONFIGURACIÓN DE PATHS PARA llmDocs
# ==============================================================================
# Agregar rutas al path de Python para imports locales
sys.path.append(os.path.join(settings.BASE_DIR, 'llmDocs'))
sys.path.append(os.path.join(settings.BASE_DIR, 'cnnFinalPry', 'llmDocs'))

# Imports de llmDocs (con manejo de errores)
try:
    from llmDocs.main import consultar_llm
    from llmDocs.utils import buscar_contexto, armar_prompt
except ImportError as e:
    print(f"⚠️ Error importando llmDocs: {e}")
    # Funciones fallback si no se puede importar
    def consultar_llm(query):
        return f"Error: No se pudo cargar el módulo LLM. Query: {query}"
    
    def buscar_contexto(query, top_k=1):
        return f"Contexto no disponible para: {query}"
    
    def armar_prompt(contexto, pregunta):
        return f"Prompt: {contexto} - {pregunta}"

# Imports de utils locales (con manejo de errores)
try:
    from .utils import (
        consultar_llm as consultar_llm_local,
        normalizar_audio,
        limpiar_audio,
        transcribir_whisper,
        texto_a_audio,
        buscar_contexto as buscar_contexto_local,
        armar_prompt as armar_prompt_local
    )
except ImportError as e:
    print(f"⚠️ Error importando utils locales: {e}")
    # Funciones fallback
    def consultar_llm_local(query):
        return f"Error: Utils local no disponible. Query: {query}"
    
    def normalizar_audio(input_path, output_path):
        pass
    
    def limpiar_audio(input_path, output_path, noise_clip_seconds=1):
        pass
    
    def transcribir_whisper(audio_path):
        return "Error: Whisper no disponible"
    
    def texto_a_audio(text, output_path):
        pass

# ==============================================================================
# CONFIGURACIÓN DEL MODELO CNN
# ==============================================================================
MODEL_PATH = os.path.join(settings.BASE_DIR, 'waferapp', 'mi_modelo.h5')

# Cargar modelo CNN con manejo de errores
cnn_model = None
if os.path.exists(MODEL_PATH):
    try:
        cnn_model = load_model(MODEL_PATH)
        print(f"✅ Modelo CNN cargado exitosamente desde: {MODEL_PATH}")
    except Exception as e:
        print(f"❌ Error cargando modelo CNN: {e}")
        cnn_model = None
else:
    print(f"❌ No se encontró el archivo del modelo en: {MODEL_PATH}")

# Etiquetas de clasificación
CLASS_LABELS = [
    "Center", "Donut", "Edge-Loc", "Edge-Ring", "Loc",
    "Near-full", "Random", "Scratch", "None"
]

# ==============================================================================
# VISTAS PRINCIPALES
# ==============================================================================

class DashboardView(TemplateView):
    """Vista principal del dashboard."""
    template_name = "dash/dash.html"


class HomeView(TemplateView):
    """Vista principal que muestra información de modelos."""
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
        ]
        
        # Información adicional del contexto
        context['total_modelos'] = len(context['modelos'])
        context['modelo_destacado'] = max(context['modelos'], key=lambda x: float(x['accuracy'].rstrip('%')))
        
        return context


class procesoModeloView(TemplateView):
    """Vista que muestra la plantilla para el entrenamiento del modelo."""
    template_name = "modelos/procesoModelo.html"


class EntrenamientoView(TemplateView):
    """Vista que muestra la plantilla para el entrenamiento del modelo."""
    template_name = "modelos/entrena.html"


class DetallesUsoView(TemplateView):
    """Vista que muestra detalles del uso del modelo CNN."""
    template_name = "modelos/detalles.html"


class ModeloCreateView(TemplateView):
    """Vista para crear y registrar un nuevo modelo CNN."""
    template_name = "modelos/add_modelo.html"
    success_url = reverse_lazy('modelos:home')

# ==============================================================================
# VISTAS DE AUTENTICACIÓN
# ==============================================================================

class SignUpView(FormView):
    """Vista para el registro de nuevos usuarios."""
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
    """Vista para iniciar sesión de usuario."""
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

# ==============================================================================
# VISTAS DE GALERÍA
# ==============================================================================

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

# ==============================================================================
# VISTAS DE PRUEBAS CNN
# ==============================================================================

class PruebasView(LoginRequiredMixin, TemplateView):
    """Vista para realizar pruebas con el modelo CNN entrenado."""
    template_name = 'pruebas/pruebas.html'

    def get(self, request):
        """Mostrar página de pruebas con historial."""
        historial = ImagenSubida.objects.filter(usuario=request.user).order_by('-fecha_subida')[:10]
        return render(request, self.template_name, {
            'class_labels': CLASS_LABELS,
            'historial': historial
        })

    def post(self, request):
        """Procesar imagen subida y realizar predicción."""
        resultado = None
        probabilities = None
        error = None
        image_preview = None

        try:
            file = request.FILES.get('uploaded_image')
            if not file:
                error = "No se seleccionó ninguna imagen."
            elif cnn_model is None:
                error = "El modelo CNN no está disponible."
            else:
                # Procesar imagen
                img = Image.open(file).convert('RGB')
                img = img.resize((26, 26))
                img_arr = np.array(img).astype('float32') / 255.0
                x = np.expand_dims(img_arr, axis=0)

                # Realizar predicción
                prediction = cnn_model.predict(x)
                predicted_class_idx = np.argmax(prediction)
                resultado = CLASS_LABELS[predicted_class_idx]
                probabilities = {label: float(prob) for label, prob in zip(CLASS_LABELS, prediction[0])}

                # Guardar en historial
                imagen_obj = ImagenSubida.objects.create(
                    usuario=request.user,
                    imagen=file,
                    resultado=resultado
                )
                image_preview = imagen_obj.imagen.url

             # Guardar en HistorialPrediccion
                HistorialPrediccion.objects.create(
                    usuario=request.user,
                    imagen=imagen_obj.imagen,
                    resultado=resultado,
                    probabilidad=float(prediction[0][predicted_class_idx])
            )
                
        except Exception as e:
            error = f"Error procesando imagen: {str(e)}"

        # Obtener historial actualizado
        historial = ImagenSubida.objects.filter(usuario=request.user).order_by('-fecha_subida')[:10]

        context = {
            'resultado': resultado,
            'probabilities': probabilities,
            'class_labels': CLASS_LABELS,
            'error': error,
            'image_preview': image_preview,
            'historial': historial,
        }
        return render(request, self.template_name, context)
    
class HistorialView(LoginRequiredMixin, ListView):
        model = HistorialPrediccion
        template_name = 'pruebas/historial.html'
        context_object_name = 'historial'

        def get_queryset(self):
        # Solo muestra el historial del usuario autenticado, ordenado por fecha descendente
            return HistorialPrediccion.objects.filter(usuario=self.request.user).order_by('-fecha')


# ==============================================================================
# VISTAS DE LLM
# ==============================================================================

class llmView(TemplateView):
    """Vista básica para el LLM."""
    template_name = "modelos/llm/llm.html"
    form_class = LLMChatForm


class LLMDesdeModelosView(FormView):
    """Vista para interactuar con el LLM desde modelos."""
    template_name = "llm/llm.html"
    form_class = LLMChatForm
    success_url = reverse_lazy("modelos:llm/llm")

    def form_valid(self, form):
        question = form.cleaned_data["question"]
        try:
            respuesta = consultar_llm_local(question)
        except Exception as e:
            respuesta = f"Error al consultar el LLM: {e}"
        
        # Devolver formulario vacío para limpiar el campo
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

# ==============================================================================
# VISTAS DE API Y PROCESAMIENTO
# ==============================================================================

@csrf_exempt
def procesar_imagen(request):
    """API para procesar imágenes con CNN y LLM."""
    if request.method == 'POST' and request.FILES.get('image'):
        if cnn_model is None:
            return JsonResponse({"error": "Modelo CNN no disponible."}, status=500)
            
        image_file = request.FILES['image']
        
        try:
            # Guardar imagen
            image_path = default_storage.save('uploads/' + image_file.name, image_file)
            image_url = default_storage.url(image_path)

            # Preprocesar imagen
            img = Image.open(image_file).convert('RGB').resize((26, 26))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Realizar predicción
            pred = cnn_model.predict(img_array)
            clase_idx = int(np.argmax(pred))
            etiqueta = CLASS_LABELS[clase_idx]

            # Consultar LLM para información adicional
            try:
                contexto = buscar_contexto_local(etiqueta, top_k=1)
                prompt = armar_prompt_local(contexto, f"El defecto es '{etiqueta}'. ¿Qué significa este defecto y qué acciones se recomiendan?")
                respuesta_llm = consultar_llm_local(prompt)
            except Exception as e:
                print(f"Error con LLM: {e}")
                respuesta_llm = f"Defecto detectado: {etiqueta}"

            return JsonResponse({
                "image_url": image_url,
                "respuesta": f"🟢 Clasificación: <b>{etiqueta}</b><br>{respuesta_llm}"
            })
            
        except Exception as e:
            return JsonResponse({"error": f"Error procesando imagen: {str(e)}"}, status=500)
    
    return JsonResponse({"error": "No se envió una imagen válida."}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ProcesarAudioView(View):
    """Vista para procesar audio con speech-to-text y LLM."""
    
    def post(self, request):
        audio_file = request.FILES.get('audio')
        ruido_segundos = int(request.POST.get('ruido_segundos', 1))

        if not audio_file:
            return JsonResponse({'error': 'No se recibió archivo de audio'}, status=400)

        # Crear directorio para audios
        audio_dir = os.path.join(settings.MEDIA_ROOT, "audios")
        os.makedirs(audio_dir, exist_ok=True)
        
        # Verificar tamaño del archivo
        if audio_file.size == 0:
            return JsonResponse({'error': 'El archivo de audio está vacío'}, status=400)
        
        input_raw = os.path.join(audio_dir, 'input_raw.wav')
        
        try:
            # Guardar archivo de audio
            with open(input_raw, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            
            # Verificar que se guardó correctamente
            if not os.path.exists(input_raw) or os.path.getsize(input_raw) == 0:
                return JsonResponse({'error': 'Error al guardar el archivo de audio'}, status=500)
            
        except Exception as e:
            return JsonResponse({'error': f'Error al guardar audio: {e}'}, status=500)

        # Convertir a formato estándar
        input_wav = os.path.join(audio_dir, 'input.wav')
        try:
            audio = AudioSegment.from_file(input_raw)
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            audio.export(input_wav, format='wav')
            
        except Exception as e:
            return JsonResponse({'error': f'Error al convertir audio: {e}. Intenta grabar de nuevo.'}, status=500)

        # Procesar audio
        try:
            wav_norm = os.path.join(audio_dir, "input_norm.wav")
            wav_limpio = os.path.join(audio_dir, "input_limpio.wav")
            
            normalizar_audio(input_wav, wav_norm)
            limpiar_audio(wav_norm, wav_limpio, noise_clip_seconds=ruido_segundos)
            
            pregunta = transcribir_whisper(wav_limpio)
            if not pregunta.strip():
                return JsonResponse({'error': 'No se detectó voz en el audio. Intenta hablar más claro.'})
            
            # Consultar LLM
            respuesta = consultar_llm_local(pregunta)
            
            # Generar audio de respuesta
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


@csrf_exempt
def api_llm_text(request):
    """API para consultas de texto al LLM."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "")
            
            if not question.strip():
                return JsonResponse({"error": "Pregunta vacía"}, status=400)
                
            respuesta = consultar_llm_local(question)
            return JsonResponse({"respuesta": respuesta})
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)