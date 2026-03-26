# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from evaluacion.models import Resultado
# from .models import Perfil
# from django.core.mail import send_mail


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             if user.is_staff:
#                 return redirect('panel_admin')
#             else:
#                 return redirect('panel_candidato')
#         else:
#             messages.error(request, 'Usuario o contraseña incorrectos')

#     return render(request, 'gestion/login.html')


# @login_required
# def panel_admin(request):
#     if not request.user.is_staff:
#         return redirect('login')

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')
#         cedula = request.POST.get('cedula')
#         foto = request.FILES.get('foto')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Ese usuario ya existe')
#         else:
#             user = User.objects.create_user(
#                 username=username,
#                 password=password,
#                 email=email
#             )

#             perfil, created = Perfil.objects.get_or_create(user=user)
#             perfil.cedula = cedula

#             if foto:
#                 perfil.foto = foto

#             perfil.save()
#             messages.success(request, 'Candidato creado correctamente')

#     resultados = Resultado.objects.select_related('usuario', 'examen')

#     return render(request, 'gestion/panel_admin.html', {
#         'resultados': resultados
#     })


# @login_required
# def panel_candidato(request):
#     resultados = Resultado.objects.filter(usuario=request.user)
#     perfil = Perfil.objects.filter(user=request.user).first()

#     return render(request, 'gestion/panel_candidato.html', {
#         'resultados': resultados,
#         'perfil': perfil
#     })


# def logout_view(request):
#     logout(request)
#     return redirect('login')




# def enviar_correo(request):
#     send_mail(
#     subject='Bienvenido a mi app',
#     message='Usted ha sido seleccionado para presentar una prueba, a continuacion su password y username para.',
#     from_email='tu_correo@gmail.com',
#     recipient_list=['destinatario@ejemplo.com']
#     )


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from evaluacion.models import Resultado
from .models import Perfil
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.rol == 'ADMIN':
                return redirect('panel_admin')
            else:
                return redirect('panel_candidato')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'gestion/login.html')


@login_required
def panel_admin(request):
    if request.user.rol != 'ADMIN':
        return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        cedula = request.POST.get('cedula')
        foto = request.FILES.get('foto')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese usuario ya existe')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                rol='CANDIDATO'
            )

            perfil, created = Perfil.objects.get_or_create(user=user)
            perfil.cedula = cedula

            if foto:
                perfil.foto = foto

            perfil.save()

            # 🔥 ENVIAR CORREO AUTOMÁTICO
            asunto = "Credenciales de acceso - Sistema de Evaluación"

            mensaje = f"""
Hola {username},

Tu cuenta ha sido creada exitosamente.

Usuario: {username}
Contraseña: {password}

Puedes ingresar al sistema desde:
http://127.0.0.1:8000/

Saludos,
Equipo de Evaluación
"""

            try:
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Candidato creado y correo enviado correctamente')
            except Exception as e:
                messages.warning(request, 'Candidato creado, pero el correo no pudo enviarse')
                print("Error enviando correo:", e)

    resultados = Resultado.objects.select_related('usuario', 'examen')

    return render(request, 'gestion/panel_admin.html', {
        'resultados': resultados
    })



@login_required
def panel_candidato(request):
    if request.user.rol != 'CANDIDATO':
        return redirect('login')

    resultados = Resultado.objects.filter(usuario=request.user)
    perfil = Perfil.objects.filter(user=request.user).first()

    return render(request, 'gestion/panel_candidato.html', {
        'resultados': resultados,
        'perfil': perfil
    })


def logout_view(request):
    logout(request)
    return redirect('login')

