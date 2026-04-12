from django.shortcuts import render
from django.db import transaction
from django.utils import timezone
from .models import Versiculo, ControleDiario, VersiculoUsado
import random


def versiculo_unico(request):
    hoje = timezone.now().date()

    controle, _ = ControleDiario.objects.get_or_create(data=hoje)

    # 👉 SE NÃO CLICOU AINDA
    if request.method != 'POST':
        total = Versiculo.objects.count()

        return render(request, 'versiculo.html', {
            'texto': '',
            'referencia': '',
            'numero': controle.contador,
            'total': total,
            'disponiveis': total - controle.contador,
            'acabou': False,
            'inicial': True
        })

    # 👉 SE CLICOU
    with transaction.atomic():

        usados_ids = VersiculoUsado.objects.filter(
            data=hoje
        ).values_list('versiculo_id', flat=True)

        disponiveis = Versiculo.objects.exclude(id__in=usados_ids)

        if not disponiveis.exists():
            total = Versiculo.objects.count()

            return render(request, 'versiculo.html', {
                'texto': 'Todos os versículos já foram entregues hoje 🙏',
                'referencia': '',
                'numero': controle.contador,
                'total': total,
                'disponiveis': 0,
                'acabou': True
            })

        escolhido = random.choice(list(disponiveis))

        VersiculoUsado.objects.create(
            data=hoje,
            versiculo=escolhido
        )

        controle.contador += 1
        controle.save()

    total = Versiculo.objects.count()

    return render(request, 'versiculo.html', {
        'texto': escolhido.texto,
        'referencia': escolhido.referencia,
        'numero': controle.contador,
        'total': total,
        'disponiveis': total - controle.contador,
        'acabou': False
    })
    