from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.serializers.auth import AuthRefreshSerializer, AuthSerializer

User = get_user_model()


class AuthView(TokenObtainPairView):
    serializer_class = AuthSerializer


class AuthRefreshView(TokenRefreshView):
    serializer_class = AuthRefreshSerializer
