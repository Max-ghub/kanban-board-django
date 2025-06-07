from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.serializers.auth import (
    AuthenticationRefreshSerializer,
    AuthenticationSerializer,
)

User = get_user_model()


class AuthenticationView(TokenObtainPairView):
    serializer_class = AuthenticationSerializer
    pass


class AuthenticationRefreshView(TokenRefreshView):
    serializer_class = AuthenticationRefreshSerializer
    pass
