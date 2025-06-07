from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.jwt import generate_tokens
from users.serializers.register import (
    RegisterUserSerializer,
    RegisterVerifyUserSerializer,
)

User = get_user_model()


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Код отправлен"}, status=status.HTTP_200_OK)


class RegisterVerifyUserView(APIView):
    def post(self, request):
        serializer = RegisterVerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = generate_tokens(user)
        return Response(data=tokens, status=status.HTTP_200_OK)
