from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Post
from account.mixins import SuperUserRequiredMixin, VerifiedUserRequiredMixin
from .mixins import PostOwnerRequiredMixin
from .forms import CategoryForm, PostForm


class CategoryListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = Category
    queryset = model.objects.all()
    context_object_name = "categories"
    template_name = "blog/categories.html"


class CategoryCreateView(LoginRequiredMixin, SuperUserRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("category:list")
    template_name = "blog/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Category added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Category update failed.")
        return redirect("category:list")


class CategoryUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("category:list")
    template_name = "blog/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Category update failed.")
        return redirect("category:list")


class CategoryDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("category:list")
    template_name = "blog/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Category deleted successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Category delete failed.")
        return redirect("category:list")


class PostCreateView(LoginRequiredMixin, VerifiedUserRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("post:list")
    template_name = "blog/post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["status"] = "create"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post published successfully.")
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    queryset = Post.objects.select_related("author").select_related("category").prefetch_related("comments").all()
    context_object_name = "posts"
    template_name = "blog/posts.html"
    paginate_by = 10


class PostUpdateView(LoginRequiredMixin, VerifiedUserRequiredMixin, PostOwnerRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("post:list")
    template_name = "blog/post_form.html"

    def get_queryset(self):
        return self.model.objects.select_related("category").select_related("author").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["post_category"] = self.get_object().category or "---"
        context["status"] = "update"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Post update failed.")
        return redirect("post:list")


class PostDeleteView(LoginRequiredMixin, VerifiedUserRequiredMixin, PostOwnerRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post:list")
    template_name = "blog/posts.html"

    def form_valid(self, form):
        messages.success(self.request, "Post deleted successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Post delete failed.")
        return redirect("category:list")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_queryset(self):
        return self.model.objects.select_related("category").select_related("author").prefetch_related("comments").all()
