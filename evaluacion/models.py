from django.db import models
from django.conf import settings


class Examen(models.Model):
    titulo = models.CharField(max_length=100)
    fecha = models.DateField()

    def __str__(self):
        return self.titulo


class Resultado(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    puntaje = models.IntegerField()

    def __str__(self):
        return f"{self.usuario} - {self.examen}"

class Pregunta(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)

    opcion_a = models.CharField(max_length=100)
    opcion_b = models.CharField(max_length=100)
    opcion_c = models.CharField(max_length=100)

    RESPUESTAS = (
        ('A', 'Opción A'),
        ('B', 'Opción B'),
        ('C', 'Opción C'),
    )

    correcta = models.CharField(max_length=1, choices=RESPUESTAS)

    def __str__(self):
        return self.texto







