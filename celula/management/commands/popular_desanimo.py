from django.core.management.base import BaseCommand
from celula.models import TemaPergunta, Pergunta


PERGUNTAS_DESANIMO = [

    # =========================
    # QUIZ (3)
    # =========================
    {
        'tipo': 'quiz',
        'texto': 'Qual versículo desta lição traz a ordem: "Sê forte e corajoso; não temas"?',
        'versiculo': '',
        'reflexao': 'A coragem bíblica não nasce da ausência de medo, mas da certeza da presença de Deus conosco.',
        'opcao_a': 'Mateus 11:28',
        'opcao_b': 'Jeremias 20:9',
        'opcao_c': 'Josué 1:9',
        'opcao_d': 'Salmo 23:1',
        'resposta_correta': 'C',
    },
    {
        'tipo': 'quiz',
        'texto': 'Em Jeremias 20:9, a Palavra de Deus é comparada a quê dentro do profeta?',
        'versiculo': 'Jeremias 20:9',
        'reflexao': 'Mesmo em tempos difíceis, Deus mantém aceso dentro de nós aquilo que Ele começou.',
        'opcao_a': 'Uma luz distante',
        'opcao_b': 'Fogo ardente nos ossos',
        'opcao_c': 'Água no deserto',
        'opcao_d': 'Vento suave',
        'resposta_correta': 'B',
    },
    {
        'tipo': 'quiz',
        'texto': 'Segundo Mateus 11:28-30, quem Jesus convida para receber descanso?',
        'versiculo': 'Mateus 11:28-30',
        'reflexao': 'Jesus não exige perfeição parComo seu projeto Moriá roda em Django com Channels, certifique-se de que o seu consumers.py está enviando o booleano correta dentro do dicionário msg no evento resposta_confirmada.a receber alguém. Ele chama os cansados e sobrecarregados.',
        'opcao_a': 'Somente os fortes',
        'opcao_b': 'Somente os líderes',
        'opcao_c': 'Os ricos e poderosos',
        'opcao_d': 'Os cansados e sobrecarregados',
        'resposta_correta': 'D',
    },

    # =========================
    # REFLEXÃO (3)
    # =========================
    {
    'tipo': 'reflexao',
    'texto': 'Às vezes o desânimo bate à porta. Como você prefere lidar com esse sentimento hoje?',
    'versiculo': 'Salmos 42:11 — "Por que você está assim tão triste, ó minha alma? Por que está assim tão perturbada dentro de mim? Ponha a sua esperança em Deus."',
    'reflexao': 'Não há problema em não estar bem. O importante é saber que você não precisa carregar esse fardo sozinho.',
    'opcao_a': 'Quero identificar o que me desanima',
    'opcao_b': 'Prefiro apenas silenciar e descansar',
    'opcao_c': 'Gostaria de uma palavra de encorajamento',
    'opcao_d': 'Prefiro guardar para mim agora',
    'resposta_correta': 'TODAS',
    },
    {
        'tipo': 'reflexao',
        'texto': 'Quando o cansaço chega, qual costuma ser sua primeira reação?',
        'versiculo': '',
        'reflexao': 'Muitas vezes buscamos soluções imediatas, mas Deus nos convida a descansar nEle.',
        'opcao_a': 'Me isolo',
        'opcao_b': 'Continuo no automático',
        'opcao_c': 'Busco oração',
        'opcao_d': 'Peço ajuda a alguém',
        'resposta_correta': '',
    },
    {
        'tipo': 'reflexao',
        'texto': 'O que mais tem roubado sua motivação ultimamente?',
        'versiculo': '',
        'reflexao': 'Identificar a origem do peso ajuda a entregar isso nas mãos de Cristo.',
        'opcao_a': 'Frustrações',
        'opcao_b': 'Sobrecarga',
        'opcao_c': 'Medo do futuro',
        'opcao_d': 'Comparações',
        'resposta_correta': '',
    },

    # =========================
    # DESAFIO (3)
    # =========================
    {
        'tipo': 'desafio',
        'texto': 'Qual área você decidiu não abandonar nesta semana?',
        'versiculo': 'Jeremias 20:9',
        'reflexao': 'Perseverar não é sentir vontade sempre. É continuar mesmo quando está difícil.',
        'opcao_a': 'Vida com Deus',
        'opcao_b': 'Família',
        'opcao_c': 'Projeto / trabalho',
        'opcao_d': 'Saúde emocional',
        'resposta_correta': '',
    },
    {
        'tipo': 'desafio',
        'texto': 'Escolha uma atitude prática para renovar seu ânimo hoje.',
        'versiculo': 'Mateus 11:28',
        'reflexao': 'Pequenos passos de obediência produzem grandes mudanças no coração.',
        'opcao_a': 'Separar tempo de oração',
        'opcao_b': 'Descansar corretamente',
        'opcao_c': 'Conversar com alguém de confiança',
        'opcao_d': 'Retomar algo importante',
        'resposta_correta': '',
    },
    {
        'tipo': 'desafio',
        'texto': 'Qual versículo você vai carregar no coração esta semana?',
        'versiculo': 'Josué 1:9; Jeremias 20:9; Mateus 11:28',
        'reflexao': 'A Palavra sustenta a mente quando as emoções vacilam.',
        'opcao_a': 'Josué 1:9',
        'opcao_b': 'Jeremias 20:9',
        'opcao_c': 'Mateus 11:28',
        'opcao_d': 'Vou memorizar os três',
        'resposta_correta': '',
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
        