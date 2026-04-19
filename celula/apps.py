from django.apps import AppConfig
from django.db.models.signals import post_migrate


def criar_grupos(sender, **kwargs):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name='membros')
    Group.objects.get_or_create(name='lideres')


class CelulaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celula'
    verbose_name = 'Célula Moriá'

    def ready(self):
        post_migrate.connect(criar_grupos, sender=self, dispatch_uid='celula_criar_grupos')

    