from rest_framework import serializers
from yellot_mob.modules.chat.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ChatMessage
        fields = "__all__"
