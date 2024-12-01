import jwt
from channels.auth import BaseMiddleware
from channels.db import database_sync_to_async
from django.conf import settings


class JwtAuthMiddleware(BaseMiddleware):
    async def connect(self):
        token = self.scope.get("headers", {}).get(b"authorization", None)
        if token:
            token = token.decode().split(" ")[1]

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = await self.get_user(payload["user_id"])
                self.scope["user"] = user
            except jwt.ExpiredSignatureError:
                await self.close()
                return
            except jwt.InvalidTokenError:
                await self.close()
                return

        await super().connect()

    @database_sync_to_async
    def get_user(self, user_id):
        from django.contrib.auth.models import User

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
