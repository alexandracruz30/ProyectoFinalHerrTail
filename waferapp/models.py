from django.db import models


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

