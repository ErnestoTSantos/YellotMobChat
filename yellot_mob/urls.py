from django.contrib import admin
from django.urls import path
from django.urls import include

from yellot_mob.modules.users.urls import urlpatterns as user_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(user_router)),
]
