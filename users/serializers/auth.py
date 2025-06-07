from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class AuthenticationSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except AuthenticationFailed:
            raise AuthenticationFailed(detail={"error": "Неверный логин или пароль"})


class AuthenticationRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except TokenError:
            raise AuthenticationFailed(
                detail={
                    "error": "Недействительный или просроченный токен",
                }
            )
