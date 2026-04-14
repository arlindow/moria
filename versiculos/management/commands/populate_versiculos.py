from django.core.management.base import BaseCommand
from versiculos.models import Versiculo


class Command(BaseCommand):
    help = 'Popula os versículos no banco de dados'

    def handle(self, *args, **kwargs):
        lista = [
            (
                "Não temas, porque eu sou contigo; não te assombres, porque eu sou o teu Deus; eu te fortaleço, e te ajudo, e te sustento com a destra da minha justiça.",
                "Isaías 41:10"
            ),
            (
                "Não fui eu que lhe ordenei? Seja forte e corajoso! Não se apavore nem desanime, pois o Senhor, o seu Deus, estará com você por onde você andar.","Josué 1:9"
            ),
            (
                "Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque tu estás comigo; a tua vara e o teu cajado me consolam.",
                "Salmos 23:4"
            ),
            (
                "Porque Deus não nos deu o espírito de temor, mas de poder, de amor e de moderação.",
                "2 Timóteo 1:7"
            ),
            (
                "No amor não há medo; ao contrário, o perfeito amor expulsa o medo, porque o medo envolve castigo. Aquele que tem medo não está aperfeiçoado no amor.",
                "1 João 4:18"
            ),
            (
                "Deixo-vos a paz, a minha paz vos dou; não vo-la dou como o mundo a dá. Não se turbe o vosso coração, nem se atemorize.",
                "João 14:27"
            ),
            (
                "Em me vindo o temor, hei de confiar em ti.","Salmos 56:3"
            ),
            (
                "Porque não recebestes o espírito de escravidão, para viverdes outra vez atemorizados, mas recebestes o Espírito de adoção, pelo qual clamamos: Aba, Pai.", "Romanos 8:15"
            ),
            (
                "Sejam fortes e corajosos. Não tenham medo nem fiquem apavorados por causa delas, pois o Senhor, o seu Deus, vai com vocês; nunca os deixará, nunca os abandonará.","Deuteronômio 31:6"
            ),
            (
                "O Senhor é a minha luz e a minha salvação; de quem terei medo? O Senhor é a fortaleza da minha vida; a quem temerei?", "Salmos 27:1"
            ),
            (
                "Mas agora, assim diz o Senhor, aquele que o criou, ó Jacó, aquele que o formou, ó Israel: Não tema, pois eu o resgatei; eu o chamei pelo nome; você é meu.", "Isaías 43:1"
            ),
            (
                "Busquei o Senhor, e ele me respondeu; livrou-me de todos os meus temores.","Salmos 34:4"
            ),
            (
                "Podemos, pois, dizer com confiança: O Senhor é o meu ajudador, não temerei; que me poderá fazer o homem?",
                "Hebreus 13:6"
            ),
            (
                "Portanto, não se preocupem com o amanhã, pois o amanhã trará as suas próprias preocupações. Basta a cada dia o seu próprio mal.",
                "Mateus 6:34"
            ),
            (
                "Ouvindo Jesus o que era falado, disse ao dirigente da sinagoga: Não tenha medo; tão somente creia.",
                "Marcos 5:36"
            ),
            (
                "Eis que Deus é a minha salvação; confiarei e não temerei, porque o Senhor Deus é a minha força e o meu cântico; ele se tornou a minha salvação.",
                "Isaías 12:2"
            ),
            (
                "O Senhor está comigo; não temerei. O que me pode fazer o homem?",
                "Salmos 118:6"
            ),
            (
                "Tu te aproximaste no dia em que te invoquei; disseste: Não temas.",
                "Lamentações 3:57"
            ),
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