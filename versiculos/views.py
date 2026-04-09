from django.shortcuts import render
from django.db import transaction
from .models import Versiculo, Contador

def versiculo_unico(request):
    contador, _ = Contador.objects.get_or_create(id=1)

    with transaction.atomic():
        disponiveis = Versiculo.objects.select_for_update().filter(usado=False)

        # 🚨 Se acabou tudo
        if not disponiveis.exists():
            return render(request, 'versiculo.html', {
                'texto': 'Todos os versículos já foram entregues hoje 🙏',
                'referencia': '',
                'numero': contador.total,
                'acabou': True
            })

        # Escolhe um disponível
        escolhido = disponiveis.order_by('?').first()

        escolhido.usado = True
        escolhido.save()

        contador.total += 1
        contador.save()

    total = Versiculo.objects.count()
    disponiveis_count = Versiculo.objects.filter(usado=False).count()

    return render(request, 'versiculo.html', {
        'texto': escolhido.texto,
        'referencia': escolhido.referencia,
        'numero': contador.total,
        'total': total,
        'disponiveis': disponiveis_count,
        'acabou': False
    })