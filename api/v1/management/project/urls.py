from rest_framework.routers import DefaultRouter

from management.views.project import ProjectViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = router.urls
