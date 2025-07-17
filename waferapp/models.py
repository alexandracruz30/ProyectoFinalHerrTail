"""Vista que muestra una lista de modelos CNN registrados en la base de datos."""
from django.db import models
from django.contrib.auth.models import User

class ModeloCNN(models.Model):
    """para registrar en la base de datos."""
    nombre = models.CharField(max_length=100)
    accuracy = models.CharField(max_length=10)
    descripcion = models.TextField()

def __str__(self):
    return str(self.nombre)

class HistorialPrediccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='historial/')
    resultado = models.CharField(max_length=100)
    probabilidad = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.resultado} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
class ImagenSubida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imagenes_subidas')
    imagen = models.ImageField(upload_to='imagenes_historial/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=255, blank=True, null=True)  # si quieres guardar la predicción

    def __str__(self):
        return f"{self.usuario.username} - {self.imagen.url} - {self.fecha_subida.strftime('%Y-%m-%d %H:%M')}"
