from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = "Cria 30 usuários no grupo membros"

    def handle(self, *args, **kwargs):
        grupo, criado = Group.objects.get_or_create(name='membros')

        senha_padrao = '@moria1284'
        total_criados = 0

        for i in range(1, 31):
            username = f'@teste{i}'

            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Usuário {username} já existe.')
                )
                continue

            user = User.objects.create_user(
                username=username,
                password=senha_padrao
            )

            user.groups.add(grupo)
            user.save()

            total_criados += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuário criado: {username} | senha: {senha_padrao}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nProcesso concluído. {total_criados} usuário(s) criado(s).'
            )
        )
        