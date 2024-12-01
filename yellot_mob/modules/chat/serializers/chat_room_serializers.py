from rest_framework import serializers
from yellot_mob.modules.chat.models import ChatRoom


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"

    def validate_name(self, value):
        if " " in value:
            raise serializers.ValidationError("Room name cannot contain spaces")

        if "-" in value:
            raise serializers.ValidationError("Room name cannot contain hyphens")

        if ChatRoom.objects.filter(name=value).exists():
            raise serializers.ValidationError("Room name already exists")
        return value
