from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from core.utils.cache import cache_response
from users.models import User
from users.serializers.user import UserSerializer


@method_decorator(cache_response(ttl=60), name="list")
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
