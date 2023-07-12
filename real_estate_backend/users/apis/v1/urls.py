from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from users.apis.v1.views import (
    UserCreateAPIView,
    UserChangePasswordAPIView,
)

app_name = "users"

urlpatterns = [
    path("register", UserCreateAPIView.as_view(), name="register"),
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("password/change", UserChangePasswordAPIView.as_view(),
         name="password_change"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
]
