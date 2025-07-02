from rest_framework.routers import DefaultRouter
from blog.api.v1.views import CategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")

app_name = "api-v1"

urlpatterns = []

urlpatterns += router.urls
