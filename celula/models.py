from django.db import models
from django.utils import timezone
import random
import string


def gerar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# ─── Conteúdo da Célula ───────────────────────────────────────────────────────

class Versiculo(models.Model):
    referencia = models.CharField(max_length=100, verbose_name='Referência')
    texto = models.TextField(verbose_name='Texto')
    ativo = models.BooleanField(default=True, verbose_name='Versículo da semana')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Versículo'
        verbose_name_plural = 'Versículos'
        ordering = ['-criado_em']

    def __str__(self):
        return self.referencia

    def save(self, *args, **kwargs):
        if self.ativo:
            Versiculo.objects.filter(ativo=True).update(ativo=False)
        super().save(*args, **kwargs)


class Reuniao(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    data = models.DateTimeField(verbose_name='Data e hora')
    local = models.CharField(max_length=200, blank=True, verbose_name='Local')
    link_online = models.URLField(blank=True, verbose_name='Link online')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reunião'
        verbose_name_plural = 'Reuniões'
        ordering = ['data']

    def __str__(self):
        return f'{self.titulo} – {self.data.strftime("%d/%m/%Y")}'

    @property
    def proxima(self):
        return self.data >= timezone.now()


class PedidoOracao(models.Model):
    SITUACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('respondido', 'Respondido'),
        ('arquivado', 'Arquivado'),
    ]
    nome = models.CharField(max_length=100, verbose_name='Nome')
    pedido = models.TextField(verbose_name='Pedido')
    situacao = models.CharField(
        max_length=20, choices=SITUACAO_CHOICES,
        default='pendente', verbose_name='Situação'
    )
    testemunho = models.TextField(blank=True, verbose_name='Testemunho / resposta')
    anonimo = models.BooleanField(default=False, verbose_name='Anônimo')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pedido de Oração'
        verbose_name_plural = 'Pedidos de Oração'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{"Anônimo" if self.anonimo else self.nome} – {self.criado_em.strftime("%d/%m/%Y")}'

    @property
    def nome_exibido(self):
        return 'Anônimo' if self.anonimo else self.nome


class Aviso(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    texto = models.TextField(verbose_name='Texto')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo


# ─── Jogo: Enfrenta o Medo ───────────────────────────────────────────────────

class TemaPergunta(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Tema')
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'

    def __str__(self):
        return self.nome


class Pergunta(models.Model):
    TIPO_CHOICES = [
        ('quiz', 'Quiz bíblico'),
        ('reflexao', 'Reflexão pessoal'),
        ('desafio', 'Verdade ou desafio'),
    ]
    tema = models.ForeignKey(
        TemaPergunta, on_delete=models.CASCADE,
        related_name='perguntas', verbose_name='Tema'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    texto = models.TextField(verbose_name='Pergunta')
    versiculo = models.CharField(max_length=200, blank=True, verbose_name='Versículo de apoio')
    reflexao = models.TextField(verbose_name='Reflexão para o grupo')
    opcao_a = models.CharField(max_length=200, verbose_name='Opção A')
    opcao_b = models.CharField(max_length=200, verbose_name='Opção B')
    opcao_c = models.CharField(max_length=200, verbose_name='Opção C')
    opcao_d = models.CharField(max_length=200, verbose_name='Opção D')
    resposta_correta = models.CharField(
        max_length=1, blank=True,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('', 'Sem resposta certa')],
        verbose_name='Resposta correta'
    )
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pergunta'
        verbose_name_plural = 'Perguntas'

    def __str__(self):
        return f'[{self.get_tipo_display()}] {self.texto[:60]}'

    def opcoes(self):
        return [
            {'letra': 'A', 'texto': self.opcao_a},
            {'letra': 'B', 'texto': self.opcao_b},
            {'letra': 'C', 'texto': self.opcao_c},
            {'letra': 'D', 'texto': self.opcao_d},
        ]

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.get_tipo_display(),
            'texto': self.texto,
            'versiculo': self.versiculo,
            'reflexao': self.reflexao,
            'opcoes': self.opcoes(),
            'resposta_correta': self.resposta_correta,
        }


class SalaJogo(models.Model):
    STATUS_CHOICES = [
        ('aguardando', 'Aguardando jogadores'),
        ('em_jogo', 'Em jogo'),
        ('encerrada', 'Encerrada'),
    ]
    codigo = models.CharField(
        max_length=6, unique=True, default=gerar_codigo, verbose_name='Código'
    )
    tema = models.ForeignKey(
        TemaPergunta, on_delete=models.SET_NULL,
        null=True, verbose_name='Tema'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='aguardando', verbose_name='Status'
    )
    pergunta_atual = models.IntegerField(default=0, verbose_name='Pergunta atual')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sala de Jogo'
        verbose_name_plural = 'Salas de Jogo'
        ordering = ['-criado_em']

    def __str__(self):
        return f'Sala {self.codigo} – {self.get_status_display()}'

    def perguntas_do_tema(self):
        if self.tema:
            return list(self.tema.perguntas.filter(ativa=True))
        return []


class Jogador(models.Model):
    sala = models.ForeignKey(
        SalaJogo, on_delete=models.CASCADE,
        related_name='jogadores', verbose_name='Sala'
    )
    nome = models.CharField(max_length=100, verbose_name='Nome')
    pontos = models.IntegerField(default=0, verbose_name='Pontos')
    channel_name = models.CharField(max_length=200, blank=True)
    conectado = models.BooleanField(default=True)
    entrou_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Jogador'
        verbose_name_plural = 'Jogadores'
        ordering = ['-pontos']

    def __str__(self):
        return f'{self.nome} ({self.sala.codigo})'


class Resposta(models.Model):
    jogador = models.ForeignKey(
        Jogador, on_delete=models.CASCADE,
        related_name='respostas'
    )
    pergunta = models.ForeignKey(
        Pergunta, on_delete=models.CASCADE,
        related_name='respostas'
    )
    opcao_escolhida = models.CharField(max_length=1)
    correta = models.BooleanField(default=False)
    tempo_resposta = models.FloatField(default=0)
    respondido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['jogador', 'pergunta']
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        