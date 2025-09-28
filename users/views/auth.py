from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.throttling import AuthThrottle
from users.serializers.auth import AuthRefreshSerializer, AuthSerializer

User = get_user_model()


class AuthView(TokenObtainPairView):
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def get(self, request, *args, **kwargs):
        return render(request, "auth.html")


class AuthRefreshView(TokenRefreshView):
    serializer_class = AuthRefreshSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "authRefresh"
