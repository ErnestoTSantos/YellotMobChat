import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter
from channels.routing import ProtocolTypeRouter
from yellot_mob.modules.chat.middleware import JwtAuthMiddleware

from yellot_mob.modules.chat.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")

django.setup()
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JwtAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
