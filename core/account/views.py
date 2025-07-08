from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, RedirectView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from captcha.models import CaptchaStore
from .forms import (
    CustomSignupForm,
    CustomLoginForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    UserInfoForm,
)

from jwt_token.models import Token
from .models import User
from .mixins import VerifiedUserRequiredMixin
from .tasks import send_email


class SignUpView(FormView):
    form_class = CustomSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("account:verify-resend")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class VerificationResendView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        domain = current_site.domain
        protocol = "https" if request.is_secure() else "http"
        token = Token.make_token(request.user)

        send_email.delay(
            email=request.user.email,
            domain=domain,
            protocol=protocol,
            using_api=False,
            token=token,
            subject="Blogosphere: Email Verification",
            html_template_name="account/email/verification_resend_email.html",
            txt_template_name="account/email/verification_resend_email.txt",
        )

        messages.success(
            self.request,
            "Verification email has been sent. Please check your inbox and follow the instructions to verify your account.",
        )

        return super().get(request, *args, **kwargs)


class VerificationConfirmView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token", None)
        try:
            user = Token.validate(token)
            user.is_verified = True
            user.save()
            messages.success(self.request, "Your email has been verified successfully.")
        except ValueError as e:
            messages.error(self.request, f"Email Verification failed. {e}")
        return super().get(request, *args, **kwargs)


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "account/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")

    def form_valid(self, form):
        user: User = form.get_user()
        if not user.is_verified:
            messages.warning(
                self.request,
                "Your email has not been verified yet. Please Verify your email to access all the features.",
            )
        return super().form_valid(form)


class CustomPasswordChangeView(LoginRequiredMixin, VerifiedUserRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "account/password_change.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        messages.success(self.request, "Your password was changed successfully.")
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "account/email/password_reset_email.txt"
    html_email_template_name = "account/email/password_reset_email.html"
    subject_template_name = "account/email/password_reset_email_subject.txt"
    template_name = "account/password_reset.html"
    success_url = reverse_lazy("index")
    token_generator = Token

    def form_valid(self, form):
        messages.success(
            self.request,
            "Password reset email has been sent. Please check your inbox and follow the instructions to reset your password.",
        )
        return super().form_valid(form)


class CustomPasswordResetConfirmView(FormView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("index")
    template_name = "account/password_reset_confirm.html"

    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get("token", None)
        if token is None:
            messages.error(self.request, "Token required.")
            return HttpResponseRedirect(reverse("index"))
        self.user = self.get_user(token)
        if self.user is None:
            return HttpResponseRedirect(reverse("index"))
        return super().dispatch(request, *args, **kwargs)

    def get_user(self, token: str) -> User:
        try:
            user = Token.validate(token, deactivate=self.request.method == "POST")
        except ValueError as e:
            messages.error(self.request, str(e))
            user = None
        return user

    def form_valid(self, form):
        password = form.cleaned_data.get("new_password1")
        self.user.set_password(password)
        self.user.save()
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)


class UserInfoEditView(LoginRequiredMixin, VerifiedUserRequiredMixin, UpdateView):
    model = User
    form_class = UserInfoForm
    success_url = reverse_lazy("index")
    template_name = "account/profile_info.html"

    def get_object(self):
        return self.request.user


class CaptchaView(TemplateView):
    template_name = "account/captcha.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = CaptchaStore.generate_key()
        context["key"] = key
        return context
