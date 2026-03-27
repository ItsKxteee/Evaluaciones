#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Crear superusuario admin con contraseña fija sin pedir input
python manage.py shell -c "
from django.contrib.auth.models import User;
user, created = User.objects.get_or_create(username='admin');
user.email = 'admin@gmail.com';
user.is_superuser = True;
user.is_staff = True;
user.set_password('TuContraseñaSegura');
user.save();
"