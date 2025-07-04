from rest_framework.routers import DefaultRouter
from .views import CommentViewSet

app_name = "api-v1"

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = []

urlpatterns += router.urls
