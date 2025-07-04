from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from blog.api.v1.views import PostViewSet
from comment.api.v1.views import PostCommentsViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")

# Create a nested router for comments under posts
nested_router = routers.NestedDefaultRouter(router, r"posts", lookup="post")
nested_router.register(r"comments", PostCommentsViewSet, basename="post-comments")

app_name = "api-v1"

urlpatterns = []

urlpatterns += router.urls
urlpatterns += nested_router.urls
