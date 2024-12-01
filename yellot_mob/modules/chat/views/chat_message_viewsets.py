from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from yellot_mob.modules.chat.models import ChatRoom
from yellot_mob.modules.chat.models import ChatMessage
from yellot_mob.modules.chat.serializers.chat_message_serializers import (
    ChatMessageSerializer,
)


class ChatMessageViewSet(ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return ChatMessage.objects.filter(room__id=room_id).order_by("created_at")

    def list(self, request, *args, **kwargs):
        room_id = getattr(self, "kwargs", {}).get("room_id")

        if not ChatRoom.objects.filter(id=room_id).exists():
            return Response({"error": "Room not found."}, status=404)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
