from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from yellot_mob.modules.chat.models import ChatRoom
from yellot_mob.modules.chat.serializers.chat_room_serializers import ChatRoomSerializer


class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all().order_by("-created_at")
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
