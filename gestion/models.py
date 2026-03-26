from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('CANDIDATO', 'Candidato'),
    )

    rol = models.CharField(max_length=20, choices=ROLES, default='CANDIDATO')

    def __str__(self):
        return self.username


class Perfil(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='fotos_candidatos/', null=True, blank=True)

    def __str__(self):
        return self.user.username




