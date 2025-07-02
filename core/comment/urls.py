from django.urls import path
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = "comment"

urlpatterns = [
    path("create/<int:post_pk>/", CommentCreateView.as_view(), name="create"),
    path("<int:pk>/update/", CommentUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", CommentDeleteView.as_view(), name="delete"),
]
