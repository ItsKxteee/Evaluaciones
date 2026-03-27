#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# python manage.py createsuperuser --no-input || true

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Intentando crear superusuario: $DJANGO_SUPERUSER_USERNAME"
    python manage.py createsuperuser \
        --no-input \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || echo "El superusuario ya existe o hubo un error omitido."
fi