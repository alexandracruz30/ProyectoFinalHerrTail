"""PARA LO QUE ES ESTA CLASE NO SE LA VERDAD, MENTIRA PARA TODOS LOS 
URLS DEL APP VENGAN A VISITARLA Y MOSTRAR HTML"""
from django.urls import path, include
from .views import (
    HomeView,
    SignUpView,
    UserLoginView,
    UserLogoutView,
    ModeloCreateView,
    EntrenamientoView,
    DetallesUsoView,
    PruebasView,
    procesoModeloView,
    DashboardView,
    GaleriaView,
    LLMDesdeModelosView,
    ProcesarAudioView,
    api_llm_text,
    procesar_imagen,
    HistorialView,
)

app_name = 'modelos'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('nuevo/', ModeloCreateView.as_view(), name='add_modelo'),
    path('proceso-entrenamiento/', EntrenamientoView.as_view(), name='proceso_entrenamiento'),
    path('detalles-uso/', DetallesUsoView.as_view(), name='detalles_uso'),
    path('zona-pruebas/', PruebasView.as_view(), name='zona_pruebas'),
    path('proceso/', procesoModeloView.as_view(), name='modeloView'),
    path('dashboard/', DashboardView.as_view(), name='dash'),
    path('historial/', HistorialView.as_view(), name='historial'),
    path('galeria/', GaleriaView.as_view(), name='galeria'),
    path('llm/', LLMDesdeModelosView.as_view(), name='llm'),
    path('llm-api/', api_llm_text, name='llm_api'),          # <-- ESTA LÍNEA ES CLAVE
    path('procesar_audio/', ProcesarAudioView.as_view(), name='procesar_audio'),
    path('llm/procesar-imagen/', procesar_imagen, name='procesar_imagen'),
    path('historial/', HistorialView.as_view(), name='historial'),
    path('galeria/', GaleriaView.as_view(), name='galeria'),
]
