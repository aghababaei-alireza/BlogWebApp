from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment
from .forms import CommentForm
from .mixins import CommentOwnerRequiredMixin
from account.mixins import VerifiedUserRequiredMixin
from blog.models import Post


class CommentCreateView(LoginRequiredMixin, VerifiedUserRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def get_post_object(self):
        post_pk = self.kwargs.get("post_pk")
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return None

    def get_success_url(self):
        if self.post_object is None:
            self.post_object = self.get_post_object()
        return reverse_lazy("post:detail", kwargs={"pk": self.post_object.pk})

    def get_context_data(self, **kwargs):
        if self.post_object is None:
            self.post_object = self.get_post_object()
        context = super().get_context_data(**kwargs)
        context["post"] = self.post_object
        return context

    def dispatch(self, request, *args, **kwargs):
        self.post_object = self.get_post_object()
        if self.post_object is None:
            messages.error(self.request, "No such post.")
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance: Comment = form.instance
        instance.post = self.post_object
        instance.author = self.request.user
        return super().form_valid(form)


class CommentUpdateView(
    LoginRequiredMixin, VerifiedUserRequiredMixin, CommentOwnerRequiredMixin, UpdateView
):
    model = Comment
    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def get_success_url(self):
        url = reverse_lazy("post:detail", kwargs={"pk": self.get_object().post.pk})
        print(url)
        print(str(url))
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.get_object().post
        return context

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Comment update failed.")
        return redirect("post:list")


class CommentDeleteView(
    LoginRequiredMixin, VerifiedUserRequiredMixin, CommentOwnerRequiredMixin, DeleteView
):
    model = Comment
    template_name = "blog/post_detail.htm"

    def get_success_url(self):
        return reverse_lazy("post:detail", kwargs={"pk": self.get_object().post.pk})

    def form_valid(self, form):
        messages.success(self.request, "Comment deleted successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Comment delete failed.")
        return redirect("post:list")
