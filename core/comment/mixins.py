from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Comment


class CommentOwnerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.author != request.user:
                messages.error(request, "you don't have permision for this comment.")
                return redirect("index")
            return super().dispatch(request, *args, **kwargs)
        except Comment.DoesNotExist:
            messages.error(request, "No such comment exists.")
            return redirect("index")
