from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class VerifiedUserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, "is_verified", False):
            messages.error(request, "Your email has not been verified yet.")
            return redirect(reverse("index"))

        return super().dispatch(request, *args, **kwargs)


class SuperUserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, "is_superuser", False):
            messages.error(request, "Admin only. You don't have permision.")
            return redirect(reverse("index"))

        return super().dispatch(request, *args, **kwargs)
