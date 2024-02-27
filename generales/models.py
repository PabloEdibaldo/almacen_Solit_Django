from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    TIPO_USUARIO_CHOICES = (
        ('administrador', 'Administrador'),
        ('soporte_tecnico', 'Soporte Técnico'),
    )

    nombre = models.CharField(max_length=255)
    usuario = models.CharField(max_length=50) # Relación uno a uno con el modelo User de Django
    email = models.EmailField()
    telefono_movil = models.CharField(max_length=15)  # Supongamos un máximo de 15 caracteres para el número
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return self.nombre