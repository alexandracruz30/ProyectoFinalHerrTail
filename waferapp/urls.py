"""PARA LO QUE ES ESTA CLASE NO SE LA VERDAD, MENTIRA PARA TODOS LOS 
URLS DEL APP VENGAN A VISITARLA Y MOSTRAR HTML"""
from django.urls import path, include
from .views import (
    HomeView,
    SignUpView,
    UserLoginView,
    UserLogoutView,
    # ModeloCreateView,  # ❌ ELIMINA ESTA LÍNEA
    EntrenamientoView,
    DetallesUsoView,
    PruebasView,
    procesoModeloView,
    DashboardView,
)

app_name = 'waferapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # path('nuevo/', ModeloCreateView.as_view(), name='add_modelo'),  # ❌ COMENTA ESTA LÍNEA
    path('proceso-entrenamiento/', EntrenamientoView.as_view(), name='proceso_entrenamiento'),
    path('detalles-uso/', DetallesUsoView.as_view(), name='detalles_uso'),
    path('zona-pruebas/', PruebasView.as_view(), name='zona_pruebas'),
    path('proceso/', procesoModeloView.as_view(), name='modeloView'),
    path('dashboard/', DashboardView.as_view(), name='dash'),
]
