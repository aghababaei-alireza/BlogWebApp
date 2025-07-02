from rest_framework.viewsets import ModelViewSet
from blog.models import Category, Post
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
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
