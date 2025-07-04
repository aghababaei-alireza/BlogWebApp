from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from comment.models import Comment
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from account.api.v1.permissions import IsVerifiedOrReadOnly
from .serializers import CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .paginations import CommentPagination


class PostCommentsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    ViewSet for managing comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsVerifiedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["post", "author"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.kwargs.get("post_pk")
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        serializer.save(author=self.request.user, post_id=post_id)


class CommentViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """
    ViewSet for managing individual comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsVerifiedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["post", "author"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
