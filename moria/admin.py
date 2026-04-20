from django.contrib import admin

admin.site.site_header = 'Célula Moriá — Administração'
admin.site.site_title = 'Moriá Admin'
admin.site.index_title = 'Painel do Líder'


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
    