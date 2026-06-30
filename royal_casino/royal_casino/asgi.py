import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import usuarios.routing # <-- Importamos nuestras rutas de WebSocket

os.environ.setdefault('django.settings.module', 'royal_casino.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            usuarios.routing.websocket_urlpatterns # <-- Conectamos las rutas aquí
        )
    ),
})