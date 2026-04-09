from django.core.management.base import BaseCommand
from versiculos.models import Versiculo

class Command(BaseCommand):
    help = 'Popula os versículos no banco de dados'

    def handle(self, *args, **kwargs):
        lista = [
            ("Deus está com você — não tenha medo.", "Isaías 41:10"),
            ("Seja forte e corajoso. Deus está com você.", "Josué 1:9"),
            ("Mesmo no vale, você não está sozinho.", "Salmos 23:4"),
            ("Você não foi criado para viver com medo.", "2 Timóteo 1:7"),
            ("O amor de Deus é maior que o seu medo.", "1 João 4:18"),
            ("A paz de Jesus guarda o seu coração.", "João 14:27"),
            ("Quando o medo vier, confie em Deus.", "Salmos 56:3"),
            ("Você não é escravo do medo.", "Romanos 8:15"),
            ("Deus vai com você — não tenha medo.", "Deuteronômio 31:6"),
            ("De quem você terá medo? Deus é sua luz.", "Salmos 27:1"),
            ("Você pertence a Deus.", "Isaías 43:1"),
            ("Deus te livra dos seus medos.", "Salmos 34:4"),
            ("O Senhor é seu ajudador.", "Hebreus 13:6"),
            ("Não se preocupe com o amanhã.", "Mateus 6:34"),
            ("Não tenha medo — apenas creia.", "Marcos 5:36"),
            ("Confie em Deus e não tema.", "Isaías 12:2"),
            ("Deus está com você.", "Salmos 118:6"),
            ("Quando você clama, Deus responde: Não temas.", "Lamentações 3:57"),
        ]

        criados = 0
        for texto, ref in lista:
            _, created = Versiculo.objects.get_or_create(
                texto=texto,
                defaults={'referencia': ref}
            )
            if created:
                criados += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ {criados} versículos criados! Total: {Versiculo.objects.count()}'
        ))
