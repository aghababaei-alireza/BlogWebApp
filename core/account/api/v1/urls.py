from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    SignupAPIView,
    LoginAPIView,
    LogoutAPIView,
    VerificationResendAPIView,
    VerificationConfirmAPIView,
    PasswordChangeAPIView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
    ProfileAPIView,
)

app_name = "api-v1"

urlpatterns = [
    # Token-based authentication
    path("signup/", SignupAPIView.as_view(), name="token-signup"),
    path("login/", LoginAPIView.as_view(), name="token-login"),
    path("logout/", LogoutAPIView.as_view(), name="token-logout"),
    # JWT-based authentication
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # Verification
    path("verify/resend/", VerificationResendAPIView.as_view(), name="verify-resend"),
    path(
        "verify/confirm/<str:token>/",
        VerificationConfirmAPIView.as_view(),
        name="verify-confirm",
    ),
    # Password processing
    path("password/change/", PasswordChangeAPIView.as_view(), name="password-change"),
    path("password/reset/", PasswordResetAPIView.as_view(), name="password-reset"),
    path(
        "password/reset/confirm/<str:token>/",
        PasswordResetConfirmAPIView.as_view(),
        name="password-reset-confirm",
    ),
    # Profile
    path("profile/", ProfileAPIView.as_view(), name="profile"),
]
