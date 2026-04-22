from django.core.management.base import BaseCommand
from celula.models import Reuniao
from datetime import datetime


class Command(BaseCommand):
    help = 'Cadastrar reunião'

    def handle(self, *args, **kwargs):

        reuniao, created = Reuniao.objects.get_or_create(
            data=datetime(2026, 4, 23, 20, 0),
            defaults={
                'titulo': 'Célula Moriá',
                'local': 'Residência de Tiago e Juliana',
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Reunião criada"))
        else:
            self.stdout.write("Reunião já existe")