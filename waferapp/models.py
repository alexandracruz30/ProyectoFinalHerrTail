from django.db import models
from django.contrib.auth.models import User


class ModeloCNN(models.Model):
    """para registrar en la base de datos."""
    nombre = models.CharField(max_length=100)
    accuracy = models.CharField(max_length=10)
    descripcion = models.TextField()

    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        verbose_name = "Modelo CNN"
        verbose_name_plural = "Modelos CNN"

class HistorialPrediccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='historial/')
    resultado = models.CharField(max_length=100)
    probabilidad = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.resultado} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"