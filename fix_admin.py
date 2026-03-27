import os
import django
from django.contrib.auth import get_user_model

# Configuramos el entorno de Django
# Según tu imagen, tu carpeta de configuración es 'primer_entregable'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'primer_entregable.settings')
django.setup()

User = get_user_model()

# Obtenemos los datos de las variables de entorno que ya tienes en Render
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if not username or not password:
    print("Error: No se encontraron las variables de entorno DJANGO_SUPERUSER.")
else:
    # get_or_create busca al usuario; si no existe, lo crea con el email
    u, created = User.objects.get_or_create(username=username, defaults={'email': email})
    
    # Esto le pone la contraseña (o la actualiza si el usuario ya existía)
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()

    if created:
        print(f"✅ Usuario '{username}' creado exitosamente.")
    else:
        print(f"✅ Contraseña actualizada para el usuario '{username}'.")