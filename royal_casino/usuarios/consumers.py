import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatCasinoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtenemos el nombre de la sala desde la URL (ej. 'global' o 'slots')
        self.nombre_sala = self.scope['url_route']['kwargs']['nombre_sala']
        self.grupo_sala = f"chat_{self.nombre_sala}"

        # Unirse al grupo de la sala
        await self.channel_layer.group_add(
            self.grupo_sala,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo al desconectarse
        await self.channel_layer.group_discard(
            self.grupo_sala,
            self.channel_name
        )

    # Recibir mensaje desde el WebSocket del navegador
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mensaje = text_data_json['message']
        usuario = self.scope["user"].username if self.scope["user"].is_authenticated else "Anónimo"

        # Enviar el mensaje a todo el grupo de la sala
        await self.channel_layer.group_send(
            self.grupo_sala,
            {
                'type': 'chat_message',
                'message': mensaje,
                'user': usuario
            }
        )

    # Recibir mensaje del grupo de la sala
    async def chat_message(self, event):
        mensaje = event['message']
        usuario = event['user']

        # Enviar el mensaje de vuelta al navegador del usuario
        await self.send(text_data=json.dumps({
            'message': mensaje,
            'user': usuario
        }))