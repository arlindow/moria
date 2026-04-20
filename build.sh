#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py popular_perguntas
python manage.py collectstatic --no-input

# Criar superusuário se as variáveis de ambiente estiverem definidas
if [ -n "$SUPERUSER_USERNAME" ] && [ -n "$SUPERUSER_EMAIL" ] && [ -n "$SUPERUSER_PASSWORD" ]; then
    echo "Criando superusuário..."
    python manage.py createsuperuser --username "$SUPERUSER_USERNAME" --email "$SUPERUSER_EMAIL" --noinput
    python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='$SUPERUSER_USERNAME'); u.set_password('$SUPERUSER_PASSWORD'); u.save()"
fi
