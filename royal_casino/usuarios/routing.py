from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Nos aseguramos de que termine en /$ para que sea una ruta limpia
    re_path(r'ws/chat/(?P<nombre_sala>\w+)/$', consumers.ChatCasinoConsumer.as_asgi()),
]