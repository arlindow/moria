import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class JogoConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.codigo_sala = self.scope['url_route']['kwargs']['codigo_sala']
        self.room_group = f'jogo_{self.codigo_sala}'
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.marcar_desconectado()
        await self.channel_layer.group_discard(self.room_group, self.channel_name)
        await self.channel_layer.group_send(self.room_group, {
            'type': 'jogadores_atualizado',
        })

    async def receive(self, text_data):
        data = json.loads(text_data)
        tipo = data.get('tipo')

        if tipo == 'entrar':
            await self.handle_entrar(data)
        elif tipo == 'responder':
            await self.handle_responder(data)
        elif tipo == 'iniciar_jogo':
            await self.handle_iniciar_jogo()
        elif tipo == 'proxima_pergunta':
            await self.handle_proxima_pergunta()
        elif tipo == 'revelar':
            await self.handle_revelar()

    # ── Handlers ──────────────────────────────────────────────────────────────

    async def handle_entrar(self, data):
        nome = data.get('nome', 'Anônimo')[:100]
        jogador = await self.criar_jogador(nome)
        self.jogador_id = jogador['id']

        await self.send(json.dumps({
            'tipo': 'entrou',
            'jogador': jogador,
        }))
        await self.channel_layer.group_send(self.room_group, {
            'type': 'jogadores_atualizado',
        })

    async def handle_iniciar_jogo(self):
        sala = await self.get_sala()
        if sala['status'] != 'aguardando':
            return

        perguntas = await self.get_perguntas()
        if not perguntas:
            await self.send(json.dumps({'tipo': 'erro', 'msg': 'Nenhuma pergunta cadastrada para este tema.'}))
            return

        await self.set_sala_status('em_jogo')
        await self.channel_layer.group_send(self.room_group, {
            'type': 'enviar_pergunta',
            'indice': 0,
        })

    async def handle_responder(self, data):
        opcao = data.get('opcao', '')
        pergunta_id = data.get('pergunta_id')
        tempo = data.get('tempo', 0)

        if not hasattr(self, 'jogador_id'):
            return

        resultado = await self.salvar_resposta(pergunta_id, opcao, tempo)
        await self.send(json.dumps({
            'tipo': 'resposta_confirmada',
            'correta': resultado['correta'],
            'pontos_ganhos': resultado['pontos'],
        }))

        todos = await self.todos_responderam(pergunta_id)
        if todos:
            await self.channel_layer.group_send(self.room_group, {
                'type': 'revelar_resultado',
                'pergunta_id': pergunta_id,
            })

    async def handle_proxima_pergunta(self):
        sala = await self.get_sala()
        prox = sala['pergunta_atual'] + 1
        perguntas = await self.get_perguntas()

        if prox >= len(perguntas):
            await self.set_sala_status('encerrada')
            placar = await self.get_placar()
            await self.channel_layer.group_send(self.room_group, {
                'type': 'jogo_encerrado',
                'placar': placar,
            })
        else:
            await self.avancar_pergunta(prox)
            await self.channel_layer.group_send(self.room_group, {
                'type': 'enviar_pergunta',
                'indice': prox,
            })

    async def handle_revelar(self):
        sala = await self.get_sala()
        await self.channel_layer.group_send(self.room_group, {
            'type': 'revelar_resultado',
            'pergunta_id': await self.get_pergunta_id_atual(),
        })

    # ── Eventos do grupo ──────────────────────────────────────────────────────

    async def jogadores_atualizado(self, event):
        jogadores = await self.get_jogadores()
        await self.send(json.dumps({
            'tipo': 'jogadores_atualizados',
            'jogadores': jogadores,
        }))

    async def enviar_pergunta(self, event):
        perguntas = await self.get_perguntas()
        indice = event['indice']
        if indice >= len(perguntas):
            return
        p = perguntas[indice]
        await self.send(json.dumps({
            'tipo': 'nova_pergunta',
            'indice': indice,
            'total': len(perguntas),
            'pergunta': p,
        }))

    async def revelar_resultado(self, event):
        resultado = await self.get_resultado_pergunta(event['pergunta_id'])
        await self.send(json.dumps({
            'tipo': 'revelacao',
            **resultado,
        }))

    async def jogo_encerrado(self, event):
        await self.send(json.dumps({
            'tipo': 'fim_de_jogo',
            'placar': event['placar'],
        }))

    # ── DB helpers ────────────────────────────────────────────────────────────

    @database_sync_to_async
    def criar_jogador(self, nome):
        from .models import SalaJogo, Jogador
        sala = SalaJogo.objects.get(codigo=self.codigo_sala)
        jogador, _ = Jogador.objects.get_or_create(
            sala=sala, nome=nome,
            defaults={'channel_name': self.channel_name, 'conectado': True}
        )
        jogador.channel_name = self.channel_name
        jogador.conectado = True
        jogador.save()
        return {'id': jogador.id, 'nome': jogador.nome, 'pontos': jogador.pontos}

    @database_sync_to_async
    def marcar_desconectado(self):
        from .models import Jogador
        if hasattr(self, 'jogador_id'):
            Jogador.objects.filter(id=self.jogador_id).update(conectado=False)

    @database_sync_to_async
    def get_sala(self):
        from .models import SalaJogo
        sala = SalaJogo.objects.get(codigo=self.codigo_sala)
        return {
            'id': sala.id,
            'codigo': sala.codigo,
            'status': sala.status,
            'pergunta_atual': sala.pergunta_atual,
        }

    @database_sync_to_async
    def get_perguntas(self):
        from .models import SalaJogo
        sala = SalaJogo.objects.get(codigo=self.codigo_sala)
        return [p.to_dict() for p in sala.perguntas_do_tema()]

    @database_sync_to_async
    def get_pergunta_id_atual(self):
        from .models import SalaJogo
        sala = SalaJogo.objects.get(codigo=self.codigo_sala)
        perguntas = sala.perguntas_do_tema()
        if sala.pergunta_atual < len(perguntas):
            return perguntas[sala.pergunta_atual].id
        return None

    @database_sync_to_async
    def set_sala_status(self, status):
        from .models import SalaJogo
        SalaJogo.objects.filter(codigo=self.codigo_sala).update(status=status)

    @database_sync_to_async
    def avancar_pergunta(self, indice):
        from .models import SalaJogo
        SalaJogo.objects.filter(codigo=self.codigo_sala).update(pergunta_atual=indice)

    @database_sync_to_async
    def get_jogadores(self):
        from .models import SalaJogo
        sala = SalaJogo.objects.get(codigo=self.codigo_sala)
        return [
            {'id': j.id, 'nome': j.nome, 'pontos': j.pontos, 'conectado': j.conectado}
            for j in sala.jogadores.filter(conectado=True)
        ]

    @database_sync_to_async
    def salvar_resposta(self, pergunta_id, opcao, tempo):
        from .models import Jogador, Pergunta, Resposta
        jogador = Jogador.objects.get(id=self.jogador_id)
        pergunta = Pergunta.objects.get(id=pergunta_id)

        correta = (pergunta.resposta_correta == opcao and pergunta.resposta_correta != '')
        pontos = 0
        if correta:
            pontos = max(100, int(1000 - (tempo * 40)))

        Resposta.objects.update_or_create(
            jogador=jogador, pergunta=pergunta,
            defaults={'opcao_escolhida': opcao, 'correta': correta, 'tempo_resposta': tempo}
        )
        if pontos:
            jogador.pontos += pontos
            jogador.save()

        return {'correta': correta, 'pontos': pontos}

    @database_sync_to_async
    def todos_responderam(self, pergunta_id):
        from .models import SalaJogo, Resposta
        sala = SalaJogo.objects.get(codigo=self.codigo_sala)
        total_jogadores = sala.jogadores.filter(conectado=True).count()
        total_respostas = Resposta.objects.filter(
            pergunta_id=pergunta_id, jogador__sala=sala
        ).count()
        return total_respostas >= total_jogadores

    @database_sync_to_async
    def get_resultado_pergunta(self, pergunta_id):
        from .models import Pergunta, Resposta, SalaJogo
        sala = SalaJogo.objects.get(codigo=self.codigo_sala)
        pergunta = Pergunta.objects.get(id=pergunta_id)
        respostas = Resposta.objects.filter(pergunta=pergunta, jogador__sala=sala)

        contagem = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        for r in respostas:
            if r.opcao_escolhida in contagem:
                contagem[r.opcao_escolhida] += 1

        return {
            'pergunta': pergunta.to_dict(),
            'contagem': contagem,
            'total_respostas': respostas.count(),
        }

    @database_sync_to_async
    def get_placar(self):
        from .models import SalaJogo
        sala = SalaJogo.objects.get(codigo=self.codigo_sala)
        return [
            {'nome': j.nome, 'pontos': j.pontos}
            for j in sala.jogadores.order_by('-pontos')
        ]

        