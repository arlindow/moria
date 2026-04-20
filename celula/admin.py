from django.contrib import admin
from .models import (
    Versiculo, Reuniao, PedidoOracao, Aviso,
    TemaPergunta, Pergunta, SalaJogo, Jogador, Resposta
)


@admin.register(Versiculo)
class VersiculoAdmin(admin.ModelAdmin):
    list_display = ['referencia', 'ativo', 'criado_em']
    list_editable = ['ativo']
    search_fields = ['referencia', 'texto']


@admin.register(Reuniao)
class ReuniaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data', 'local']
    list_filter = ['data']
    search_fields = ['titulo', 'descricao']


@admin.register(PedidoOracao)
class PedidoOracaoAdmin(admin.ModelAdmin):
    list_display = ['nome_exibido', 'situacao', 'criado_em']
    list_filter = ['situacao']
    list_editable = ['situacao']
    search_fields = ['nome', 'pedido']


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ativo', 'criado_em']
    list_editable = ['ativo']


class PerguntaInline(admin.TabularInline):
    model = Pergunta
    extra = 1
    fields = ['tipo', 'texto', 'opcao_a', 'opcao_b', 'opcao_c', 'opcao_d', 'resposta_correta', 'ativa']


@admin.register(TemaPergunta)
class TemaPerguntaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    inlines = [PerguntaInline]


@admin.register(SalaJogo)
class SalaJogoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'tema', 'status', 'pergunta_atual', 'criado_em']
    list_filter = ['status', 'tema']
    search_fields = ['codigo']


@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sala', 'pontos', 'conectado']
    list_filter = ['sala', 'conectado']
    search_fields = ['nome']


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ['jogador', 'pergunta', 'opcao_escolhida', 'correta', 'tempo_resposta']
    list_filter = ['correta']
    search_fields = ['jogador__nome', 'pergunta__texto']