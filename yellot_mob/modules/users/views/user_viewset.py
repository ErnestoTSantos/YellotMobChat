from http.client import responses

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from yellot_mob.modules.users.serializers.user_serializer import UserSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Cria um novo usuário no sistema.",
        request_body=UserSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Usuário criado com sucesso.",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Erro na criação do usuário."
            ),
        },
    )
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.create(serializer.validated_data)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
