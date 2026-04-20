from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/jogo/(?P<codigo_sala>\w+)/$', consumers.JogoConsumer.as_asgi()),
]
