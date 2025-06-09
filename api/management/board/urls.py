from rest_framework.routers import DefaultRouter

from kanban_board.apps.management.views.board import BoardViewSet

router = DefaultRouter()
router.register(r"boards", BoardViewSet, basename="board")

urlpatterns = router.urls
