from django.contrib import admin

from yellot_mob.modules.chat.models import ChatRoom
from yellot_mob.modules.chat.models import ChatMessage


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    list_filter = ("name",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "created_at", "updated_at")
    list_filter = (
        "user",
        "room__name",
    )
