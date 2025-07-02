from django.urls import path, include
from blog.views import (
    PostCreateView,
    PostListView,
    PostUpdateView,
    PostDeleteView,
    PostDetailView,
)

app_name = "post"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("create/", PostCreateView.as_view(), name="create"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
    path("api/v1/", include("blog.api.v1.urls.post")),
]
