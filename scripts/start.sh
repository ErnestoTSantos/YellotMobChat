#!/usr/bin/env bash

set -e

python manage.py makemigrations
python manage.py migrate

echo "from django.contrib.auth import get_user_model; \
        user_model = get_user_model(); user, _ = user_model.objects.get_or_create(username='admin'); \
        user.set_password('admin'); user.is_staff = True; user.is_superuser = True; \
        user.save()" | python3 manage.py shell

if [[ ${DJANGO_BIND_ADDRESS+x} ]] && [[ ${DJANGO_BIND_PORT+x} ]];
then
    echo "OK! Using custom ADRESSS $DJANGO_BIND_ADDRESS and PORT $DJANGO_BIND_PORT to set Django runserver command"
    python manage.py runserver ${DJANGO_BIND_ADDRESS}:${DJANGO_BIND_PORT}
else
    echo "Using 0.0.0.0:8000 as parameter for Django runserver command"
    python manage.py runserver 0.0.0.0:8000
fi