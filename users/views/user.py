from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet

from core.utils.cache import cache_response
from users.models import User
from users.serializers.user import UserSerializer


@method_decorator(cache_response(timeout=60), "list")
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
