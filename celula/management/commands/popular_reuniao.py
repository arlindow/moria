from django.core.management.base import BaseCommand
from celula.models import Reuniao
from datetime import date


class Command(BaseCommand):
    help = 'Cadastra próximas reuniões'

    def handle(self, *args, **kwargs):

        reunioes = [
            {
                'titulo': 'Célula Moriá',
                'tema': 'Próxima Reunião',
                'data': date(2026, 4, 23),
                'hora': '20:00',
                'local': 'Residência de Tiago e Juliana',
            },
        ]

        for r in reunioes:
            obj, created = Reuniao.objects.get_or_create(
                data=r['data'],
                defaults=r
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Reunião criada para {r['data']}"
                ))
            else:
                self.stdout.write(
                    f"Já existe reunião em {r['data']}"
                )

        self.stdout.write(self.style.SUCCESS("Finalizado."))