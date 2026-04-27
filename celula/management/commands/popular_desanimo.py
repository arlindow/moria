from django.core.management.base import BaseCommand
from celula.models import TemaPergunta, Pergunta


PERGUNTAS_DESANIMO = [

    # =========================
    # QUIZ (3)
    # =========================
    {
        'tipo': 'reflexao',
        'texto': 'Qual situação mais te causa ansiedade no dia a dia?',
        'versiculo': '',
        'reflexao': 'Compartilhar nossos medos em grupo já é um ato de coragem. Em comunhão, descobrimos que ninguém precisa lutar sozinho, e que Deus fortalece cada coração.',
        'opcao_a': 'Futuro e incertezas',
        'opcao_b': 'Relacionamentos',
        'opcao_c': 'Trabalho e estudos',
        'opcao_d': 'Saúde da família',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': '',
    },
    {
        'tipo': 'quiz',
        'texto': 'Qual versículo diz: "Não andem ansiosos por coisa alguma, mas em tudo, pela oração e súplicas, e com ação de graças, apresentem seus pedidos a Deus."?',
        'versiculo': '',
        'reflexao': 'Paulo escreveu esse texto provavelmente enquanto estava preso e acorrentado, provando que a serenidade não é a ausência de tempestades, mas a presença de Deus no barco.',
        'opcao_a': 'João 14:27',
        'opcao_b': 'Filipenses 4:6',
        'opcao_c': 'Mateus 6:34',
        'opcao_d': 'Salmos 46:1',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': 'B',
    },
    {
        'tipo': 'desafio',
        'texto': 'Como você normalmente reage quando o medo chega?',
        'versiculo': '',
        'reflexao': 'Cada um de nós tem uma reação diferente, mas a prática de levar a Deus primeiro transforma gradualmente como nosso corpo e mente respondem ao medo.',
        'opcao_a': 'Oro imediatamente',
        'opcao_b': 'Evito pensar no assunto',
        'opcao_c': 'Converso com alguém',
        'opcao_d': 'Fico paralisado por um tempo',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': '',
    },
    {
        'tipo': 'quiz',
        'texto': 'Jesus disse "Não temais" (ou "não tenhais medo") quantas vezes aproximadamente nos Evangelhos?',
        'versiculo': 'Mateus 14:27; Lucas 12:7; João 14:27',
        'reflexao': 'Uma das ordens mais repetida por Jesus foi justamente esta. Se Ele precisou dizer tantas vezes, é porque o medo é real — mas também vencível com Ele.',
        'opcao_a': '3 vezes',
        'opcao_b': '10 vezes',
        'opcao_c': '18 vezes',
        'opcao_d': 'Mais de 20 vezes',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': 'D',
    },
    {
        'tipo': 'reflexao',
        'texto': 'O que mais te ajuda quando você está ansioso?',
        'versiculo': '',
        'reflexao': 'Deus criou remédios para a ansiedade: comunidade, oração, música, descanso. Todos aparecem nos Salmos. Qual você tem mais usado?',
        'opcao_a': 'Oração e Palavra',
        'opcao_b': 'Conversar com irmãos',
        'opcao_c': 'Música de louvor',
        'opcao_d': 'Silêncio e descanso',
        'opcao_e': 'Nenhuma das alternativas',
'resposta_correta': '',
    },
    {
        'tipo': 'quiz',
        'texto': '"Porque Deus não nos deu o espírito de ___, mas de poder, de amor e de moderação." Como completa?',
        'versiculo': '2 Timóteo 1:7 NVI',
        'reflexao': 'O medo não vem de Deus. Isso não significa que é fraqueza sentir medo — significa que há um Pai que quer nos equipar com algo mais forte.',
        'opcao_a': 'tristeza',
        'opcao_b': 'covardia',
        'opcao_c': 'medo',
        'opcao_d': 'fraqueza',
        'opcao_e': 'nenhuma das alternativas',
        'resposta_correta': 'B',
    },
    {
        'tipo': 'desafio',
        'texto': 'Se você pudesse deixar um medo na cruz agora, qual seria?',
        'versiculo': '1 Pedro 5:7',
        'reflexao': 'Leiam juntos: 1 Pedro 5:7 — "Lançando sobre Ele toda a vossa ansiedade, porque Ele tem cuidado de vós." O desafio é escolher um medo específico e entregar para Jesus esta semana, confiando que Ele cuida de cada detalhe.',
        'opcao_a': 'Medo de rejeição',
        'opcao_b': 'Medo do futuro',
        'opcao_c': 'Medo de fracassar',
        'opcao_d': 'Medo de perder alguém',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': '',
    },
    {
        'tipo': 'quiz',
        'texto': 'Qual Salmo começa com "O Senhor é o meu pastor, nada me faltará"?',
        'versiculo': '',
        'reflexao': 'Este Salmo foi escrito por Davi no meio de lutas reais. A confiança nele não era ingênua — era conquistada. Que tal memorizar um versículo dele esta semana?',
        'opcao_a': 'Salmo 23',
        'opcao_b': 'Salmo 91',
        'opcao_c': 'Salmo 46',
        'opcao_d': 'Salmo 121',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': 'A',
    },
]


class Command(BaseCommand):
    help = 'Popula o banco com perguntas do tema Vencendo o Desânimo'

    def handle(self, *args, **kwargs):
        tema, created = TemaPergunta.objects.get_or_create(
            nome='Vencendo o Desânimo',
            defaults={
                'descricao': 'Tema sobre renovar o ânimo, perseverar e descansar em Cristo'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Tema criado: Vencendo o Desânimo'))
        else:
            self.stdout.write('Tema já existe, adicionando perguntas...')

        for i, dados in enumerate(PERGUNTAS_DESANIMO):
            pergunta, created = Pergunta.objects.get_or_create(
                tema=tema,
                texto=dados['texto'],
                defaults=dados
            )

            status = 'criada' if created else 'já existe'
            self.stdout.write(f'Pergunta {i + 1}: {status}')

        self.stdout.write(self.style.SUCCESS(
            '\nPronto! 9 perguntas adicionadas para o tema "Vencendo o Desânimo".'
        ))
        