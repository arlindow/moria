#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py migrate --noinput

# Popular perguntas
python manage.py popular_perguntas
python manage.py popular_desanimo

# Criar usuários de teste
python manage.py populate_usuarios

# Arquivos estáticos
python manage.py collectstatic --no-input

# Criar superusuário se variáveis existirem
if [ -n "$SUPERUSER_USERNAME" ] && [ -n "$SUPERUSER_EMAIL" ] && [ -n "$SUPERUSER_PASSWORD" ]; then
    echo "Criando superusuário..."

python manage.py shell << END
from django.contrib.auth.models import User

try:
    user = User.objects.get(username='$SUPERUSER_USERNAME')
    user.set_password('$SUPERUSER_PASSWORD')
    user.email = '$SUPERUSER_EMAIL'
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"Superusuário atualizado: {user.username}")

except User.DoesNotExist:
    User.objects.create_superuser(
        '$SUPERUSER_USERNAME',
        '$SUPERUSER_EMAIL',
        '$SUPERUSER_PASSWORD'
    )
    print("Superusuário criado com sucesso.")
END

fi