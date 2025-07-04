from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from blog.models import Category, Post
from .serializers import CategorySerializer, PostSerializer
from .permissions import IsVerifiedOrReadOnly, IsAuthorOrReadOnly, IsSuperuserOrReadOnly
from .paginations import PostPagination


class CategoryViewSet(ModelViewSet):
    """
    ViewSet for managing blog categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsSuperuserOrReadOnly,
        IsVerifiedOrReadOnly,
    ]

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class PostViewSet(ModelViewSet):
    """
    ViewSet for managing blog posts.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsVerifiedOrReadOnly,
        IsAuthorOrReadOnly,
    ]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "author"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 5))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
