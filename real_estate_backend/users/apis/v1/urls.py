from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from users.apis.v1 import views


from users.apis.v1.views import (
    UserCreateAPIView,
    CustomTokenObtainPairView,
    GoogleSignInView,
    UserChangePasswordAPIView,
    PasswordResetView,
    PasswordResetConfirmView,
)

app_name = "users"

urlpatterns = [
    path("register", UserCreateAPIView.as_view(), name="register"),
    path("login", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("password/change", UserChangePasswordAPIView.as_view(),
         name="password_change"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path('google-signin', GoogleSignInView.as_view(), name='google_signin'),
    path('reset-password', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('<int:id>/', views.UserEditProfileView.as_view(), name='user_detail'),

]
