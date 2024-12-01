import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = self.scope["url_route"]["kwargs"].get("room_name", None)
            if not self.room_name:
                raise ValueError("room_name não encontrado na URL")

            self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()

        except Exception as e:
            await self.close()
            print(f"Erro ao conectar: {e}")

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            user = text_data_json["user"]

            await self.save_message(self.room_name, user, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "user": user,
                },
            )

        except KeyError as e:
            print(f"Erro ao processar mensagem: {e}")
            await self.send(
                text_data=json.dumps({"error": "Formato de mensagem inválido"})
            )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "user": user,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, room_name, user, message):
        try:
            from django.contrib.auth.models import User
            from yellot_mob.modules.chat.models import ChatRoom
            from yellot_mob.modules.chat.models import ChatMessage

            room = ChatRoom.objects.get(name=room_name)
            user_obj = User.objects.get(username=user)

            ChatMessage.objects.create(room=room, user=user_obj, message=message)

        except ObjectDoesNotExist as e:
            logger.error(f"Erro ao salvar mensagem: {e}")
            raise ValueError("Sala ou usuário não encontrados.")
