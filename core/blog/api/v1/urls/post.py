from rest_framework.routers import DefaultRouter
from blog.api.v1.views import PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")

app_name = "api-v1"

urlpatterns = []

urlpatterns += router.urls
