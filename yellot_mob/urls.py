from django.contrib import admin
from django.urls import path
from django.urls import include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

from yellot_mob.modules.users.urls import urlpatterns as user_router
from yellot_mob.modules.chat.urls import urlpatterns as chat_router

schema_view = get_schema_view(
    openapi.Info(
        title="API do Projeto",
        default_version="v1",
        description="Documentação da API do Projeto",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@exemplo.com"),
        license=openapi.License(name="Licença MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(user_router)),
    path("", include(chat_router)),
    path(
        "docs/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
