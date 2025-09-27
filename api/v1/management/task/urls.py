from rest_framework.routers import DefaultRouter

from management.views.task import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = router.urls
