from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from yellot_mob.modules.users.views.user_viewset import RegisterViewSet

router = DefaultRouter()
router.register("register", RegisterViewSet, basename="register")


urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/v1/refresh/", TokenRefreshView.as_view(), name="refresh"),
]
