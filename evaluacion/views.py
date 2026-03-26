
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Examen, Resultado
from datetime import date


@login_required
def presentar_examen(request):
    examen = Examen.objects.first()

    if not examen:
        return redirect('panel_candidato')

    if Resultado.objects.filter(usuario=request.user, examen=examen).exists():
        return redirect('panel_candidato')

    preguntas = examen.pregunta_set.all()

    if request.method == 'POST':
        puntaje = 0

        for pregunta in preguntas:
            respuesta = request.POST.get(f"pregunta_{pregunta.id}")
            if respuesta == pregunta.correcta:
                puntaje += 1

        Resultado.objects.create(
            usuario=request.user,
            examen=examen,
            puntaje=puntaje
        )

        return redirect('panel_candidato')

    return render(request, 'evaluacion/presentar_examen.html', {
        'examen': examen,
        'preguntas': preguntas
    })


