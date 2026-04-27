from django.core.management.base import BaseCommand
from celula.models import TemaPergunta, Pergunta


PERGUNTAS_MEDO = [
    {
        'tipo': 'reflexao',
        'texto': 'Qual área da sua vida mais desperta medo hoje?',
        'versiculo': '',
        'reflexao': 'Reconhecer o medo não é sinal de fraqueza. Muitas vezes, é o começo de um encontro sincero com Deus.',
        'opcao_a': 'Futuro financeiro',
        'opcao_b': 'Família e relacionamentos',
        'opcao_c': 'Saúde',
        'opcao_d': 'Propósito de vida',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': '',
    },

    {
        'tipo': 'quiz',
        'texto': 'Qual personagem bíblico enfrentou um gigante mesmo sendo jovem?',
        'versiculo': '1 Samuel 17',
        'reflexao': 'Davi não venceu Golias porque era forte, mas porque confiava em um Deus maior que o problema.',
        'opcao_a': 'José',
        'opcao_b': 'Davi',
        'opcao_c': 'Moisés',
        'opcao_d': 'Elias',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': 'B',
    },

    {
        'tipo': 'desafio',
        'texto': 'Quando o medo aparece, qual costuma ser sua primeira reação?',
        'versiculo': '',
        'reflexao': 'Nossas reações revelam onde temos buscado segurança. Deus deseja ser nosso primeiro refúgio.',
        'opcao_a': 'Orar',
        'opcao_b': 'Fugir do problema',
        'opcao_c': 'Pedir conselho',
        'opcao_d': 'Travar emocionalmente',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': '',
    },

    {
        'tipo': 'quiz',
        'texto': 'Quem caminhou sobre as águas ao encontro de Jesus?',
        'versiculo': 'Mateus 14:29',
        'reflexao': 'Enquanto Pedro olhou para Jesus, andou sobre o impossível. O medo cresce quando tiramos os olhos dEle.',
        'opcao_a': 'João',
        'opcao_b': 'Pedro',
        'opcao_c': 'Tiago',
        'opcao_d': 'Paulo',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': 'B',
    },

    {
        'tipo': 'reflexao',
        'texto': 'O que normalmente te ajuda a recuperar a paz?',
        'versiculo': '',
        'reflexao': 'Deus usa ferramentas simples para restaurar o coração: oração, descanso, comunhão e esperança.',
        'opcao_a': 'Oração',
        'opcao_b': 'Conversar com alguém',
        'opcao_c': 'Louvor',
        'opcao_d': 'Tempo sozinho com Deus',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': '',
    },

    {
        'tipo': 'quiz',
        'texto': 'Complete: "Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque..."',
        'versiculo': 'Salmo 23:4',
        'reflexao': 'A ausência de medo não vem da estrada fácil, mas da certeza da companhia de Deus.',
        'opcao_a': 'sou forte',
        'opcao_b': 'tu estás comigo',
        'opcao_c': 'vencerei tudo',
        'opcao_d': 'meus inimigos cairão',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': 'B',
    },

    {
        'tipo': 'desafio',
        'texto': 'Se você pudesse entregar um medo específico a Deus hoje, qual seria?',
        'versiculo': '1 Pedro 5:7',
        'reflexao': 'Lançar sobre Deus a ansiedade é um exercício diário de confiança.',
        'opcao_a': 'Medo do futuro',
        'opcao_b': 'Medo de fracassar',
        'opcao_c': 'Medo da rejeição',
        'opcao_d': 'Medo de perder alguém',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': '',
    },

    {
        'tipo': 'quiz',
        'texto': 'Qual versículo diz: "No amor não há medo; antes, o perfeito amor lança fora o medo"?',
        'versiculo': '1 João 4:18',
        'reflexao': 'Quanto mais conhecemos o amor de Deus, menos espaço o medo encontra em nós.',
        'opcao_a': 'Romanos 8:1',
        'opcao_b': '1 João 4:18',
        'opcao_c': 'João 3:16',
        'opcao_d': 'Filipenses 4:13',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': 'B',
    },

    {
        'tipo': 'quiz',
        'texto': 'Em Isaías 41:10, Deus ordena:',
        'versiculo': 'Isaías 41:10',
        'reflexao': 'Quando Deus diz "não temas", Ele oferece Sua presença como resposta.',
        'opcao_a': 'Pare de lutar',
        'opcao_b': 'Não temas',
        'opcao_c': 'Fique em silêncio',
        'opcao_d': 'Esconda-se',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': 'B',
    },

    {
        'tipo': 'reflexao',
        'texto': 'Se Jesus falasse algo ao seu coração hoje sobre seus medos, o que você gostaria de ouvir?',
        'versiculo': '',
        'reflexao': 'Talvez a resposta já esteja na Palavra: "Tende bom ânimo, sou eu; não temais."',
        'opcao_a': 'Estou com você',
        'opcao_b': 'Vai passar',
        'opcao_c': 'Confie em Mim',
        'opcao_d': 'Você não está sozinho',
        'opcao_e': 'Nenhuma das alternativas',
        'resposta_correta': '',
    },
]


class Command(BaseCommand):
    help = 'Popula o banco com perguntas iniciais sobre Medo e Ansiedade'

    def handle(self, *args, **kwargs):
        tema, created = TemaPergunta.objects.get_or_create(
            nome='Medo e Ansiedade',
            defaults={'descricao': 'Reunião temática sobre medo, ansiedade e a paz de Deus'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Tema criado: Medo e Ansiedade'))
        else:
            self.stdout.write('Tema já existe, adicionando perguntas...')

        for i, dados in enumerate(PERGUNTAS_MEDO):
            p, created = Pergunta.objects.get_or_create(
                tema=tema,
                texto=dados['texto'],
                defaults=dados
            )
            status = 'criada' if created else 'já existe'
            self.stdout.write(f'  Pergunta {i + 1}: {status}')

        self.stdout.write(self.style.SUCCESS(
            f'\nPronto! {len(PERGUNTAS_MEDO)} perguntas para o tema "Medo e Ansiedade".'
        ))
        self.stdout.write('Acesse /admin para ver e editar as perguntas.')
        