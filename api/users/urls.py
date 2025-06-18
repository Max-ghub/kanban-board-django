from rest_framework.routers import SimpleRouter

from users.views.user import UserViewSet

router = SimpleRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = router.urls
