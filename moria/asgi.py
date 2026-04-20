import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import moria.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moria.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(moria.routing.websocket_urlpatterns)
    ),
})