import factory
from django.contrib.auth.models import User
from yellot_mob.modules.chat.models import ChatRoom


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "password")


class ChatRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatRoom

    name = factory.Sequence(lambda n: f"Room {n}")
