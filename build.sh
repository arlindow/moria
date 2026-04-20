#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py popular_perguntas
python manage.py collectstatic --no-input

# Criar superusuário se as variáveis de ambiente estiverem definidas
if [ -n "$SUPERUSER_USERNAME" ] && [ -n "$SUPERUSER_EMAIL" ] && [ -n "$SUPERUSER_PASSWORD" ]; then
    echo "Criando superusuário..."
    python manage.py shell << END
from django.contrib.auth.models import User
try:
    user = User.objects.get(username='$SUPERUSER_USERNAME')
    user.set_password('$SUPERUSER_PASSWORD')
    user.save()
    print(f"Superusuário '{user.username}' atualizado.")
except User.DoesNotExist:
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print(f"Superusuário criado: {User.objects.get(username='$SUPERUSER_USERNAME').username}")
END
fi
