from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import (
    SignUpView,
    VerificationResendView,
    VerificationConfirmView,
    CustomLoginView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    UserInfoEditView,
)

app_name = "account"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path("edit/", UserInfoEditView.as_view(), name="edit"),
    # Password
    path("password/change/", CustomPasswordChangeView.as_view(), name="password-change"),
    path("password/reset/", CustomPasswordResetView.as_view(), name="password-reset"),
    path(
        "password/reset/confirm/<str:token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    # Verification
    path("verify/resend/", VerificationResendView.as_view(), name="verify-resend"),
    path(
        "verify/confirm/<str:token>/",
        VerificationConfirmView.as_view(),
        name="verify-confirm",
    ),
    # API
    path("api/v1/", include("account.api.v1.urls")),
]
