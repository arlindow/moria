from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from celula.models import (
    Versiculo, Reuniao, PedidoOracao, Aviso,
    SalaJogo, TemaPergunta, Jogador
)


# ─── Página principal ────────────────────────────────────────────────────────

def home(request):
    versiculo = Versiculo.objects.filter(ativo=True).first()
    reunioes = Reuniao.objects.filter(data__gte=timezone.now()).order_by('data')[:3]
    avisos = Aviso.objects.filter(ativo=True)[:4]
    pedidos = PedidoOracao.objects.filter(situacao='pendente', anonimo=False)[:5]

    return render(request, 'home.html', {
        'versiculo': versiculo,
        'reunioes': reunioes,
        'avisos': avisos,
        'pedidos': pedidos,
    })


# ─── Pedidos de oração ───────────────────────────────────────────────────────

def oracao(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        pedido = request.POST.get('pedido', '').strip()
        anonimo = request.POST.get('anonimo') == 'on'

        if nome and pedido:
            PedidoOracao.objects.create(nome=nome, pedido=pedido, anonimo=anonimo)
            messages.success(request, 'Pedido enviado! A célula vai orar por você.')
            return redirect('oracao')

    pedidos = PedidoOracao.objects.filter(situacao__in=['pendente', 'respondido'])
    return render(request, 'oracao.html', {'pedidos': pedidos})


# ─── Reuniões ─────────────────────────────────────────────────────────────────

def reunioes(request):
    proximas = Reuniao.objects.filter(data__gte=timezone.now()).order_by('data')
    passadas = Reuniao.objects.filter(data__lt=timezone.now()).order_by('-data')[:5]
    return render(request, 'reunioes.html', {
        'proximas': proximas,
        'passadas': passadas,
    })


# ─── Jogo ─────────────────────────────────────────────────────────────────────

def jogo_home(request):
    temas = TemaPergunta.objects.filter(ativo=True)
    return render(request, 'jogo/home.html', {'temas': temas})


def jogo_criar(request):
    if request.method == 'POST':
        tema_id = request.POST.get('tema_id')
        tema = get_object_or_404(TemaPergunta, id=tema_id)
        sala = SalaJogo.objects.create(tema=tema)
        return redirect('jogo_sala_lider', codigo=sala.codigo)
    return redirect('jogo_home')


def jogo_sala_lider(request, codigo):
    sala = get_object_or_404(SalaJogo, codigo=codigo)
    return render(request, 'jogo/sala_lider.html', {'sala': sala})


def jogo_entrar(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').upper().strip()
        nome = request.POST.get('nome', '').strip()
        if not codigo or not nome:
            messages.error(request, 'Preencha o código e seu nome.')
            return redirect('jogo_home')

        try:
            sala = SalaJogo.objects.get(codigo=codigo)
        except SalaJogo.DoesNotExist:
            messages.error(request, f'Sala "{codigo}" não encontrada.')
            return redirect('jogo_home')

        if sala.status == 'encerrada':
            messages.error(request, 'Esta sala já foi encerrada.')
            return redirect('jogo_home')

        return render(request, 'jogo/sala_jogador.html', {
            'sala': sala,
            'nome_jogador': nome,
        })

    return redirect('jogo_home')


# ─── API simples (JSON) ───────────────────────────────────────────────────────

def api_sala_status(request, codigo):
    sala = get_object_or_404(SalaJogo, codigo=codigo)
    jogadores = [
        {'nome': j.nome, 'pontos': j.pontos}
        for j in sala.jogadores.filter(conectado=True)
    ]
    return JsonResponse({
        'codigo': sala.codigo,
        'status': sala.status,
        'jogadores': jogadores,
        'pergunta_atual': sala.pergunta_atual,
    })