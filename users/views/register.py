from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from extra_settings.models import Setting
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.jwt import generate_tokens
from users.serializers.register import (
    RegisterUserSerializer,
    RegisterVerifyUserSerializer,
)
from users.signals import user_activated

User = get_user_model()


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "register.html")

    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        if Setting.get("OFF_REGISTER"):
            return JsonResponse(
                {"message": "Регистрация временно отключена, попробуйте позже"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Код отправлен"}, status=status.HTTP_200_OK)


class RegisterVerifyUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterVerifyUserSerializer)
    def post(self, request):
        serializer = RegisterVerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_activated.send(sender=User, user=user)

        tokens = generate_tokens(user)
        return Response(data=tokens, status=status.HTTP_200_OK)
