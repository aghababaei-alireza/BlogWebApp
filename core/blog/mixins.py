from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .models import Post


class PostOwnerRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if Post.objects.get(pk=pk).author != request.user:
            messages.error(request, "You don't have permision for this post.")
            return redirect(reverse("index"))

        return super().dispatch(request, *args, **kwargs)
