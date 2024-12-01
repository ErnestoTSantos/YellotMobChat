from rest_framework.routers import DefaultRouter
from django.urls import path, include

from yellot_mob.modules.chat.views.chat_room_viewsets import ChatRoomViewSet
from yellot_mob.modules.chat.views.chat_message_viewsets import ChatMessageViewSet

router = DefaultRouter()
router.register(r"rooms", ChatRoomViewSet, basename="chatroom")
router.register(
    r"messages/(?P<room_id>[0-9a-f-]+)", ChatMessageViewSet, basename="chatmessage"
)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
