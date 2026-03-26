from django.contrib import admin
from .models import Examen, Resultado, Pregunta


class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1


@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha')
    search_fields = ('titulo',)
    inlines = [PreguntaInline]


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'examen', 'puntaje')
    list_filter = ('examen',)
