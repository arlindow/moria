from django.contrib import admin
from celula.models import (
    Versiculo, Reuniao, PedidoOracao, Aviso,
    TemaPergunta, Pergunta, SalaJogo, Jogador, Resposta
)

admin.site.site_header = 'Célula Moriá — Administração'
admin.site.site_title = 'Moriá Admin'
admin.site.index_title = 'Painel do Líder'


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


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ['tema', 'tipo', 'texto_curto', 'ativa']
    list_filter = ['tema', 'tipo', 'ativa']
    list_editable = ['ativa']
    search_fields = ['texto']

    def texto_curto(self, obj):
        return obj.texto[:60]
    texto_curto.short_description = 'Pergunta'


class JogadorInline(admin.TabularInline):
    model = Jogador
    extra = 0
    readonly_fields = ['nome', 'pontos', 'conectado', 'entrou_em']
    can_delete = False


@admin.register(SalaJogo)
class SalaJogoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'tema', 'status', 'pergunta_atual', 'criado_em']
    list_filter = ['status', 'tema']
    readonly_fields = ['codigo', 'criado_em']
    inlines = [JogadorInline]
    