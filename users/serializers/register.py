from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from phone.models import PhoneCode

User = get_user_model()
MAX_ATTEMPTS = 5


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone", "username", "name", "surname", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterVerifyUserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs.get("phone")
        code = attrs.get("code")

        try:
            phone_code = PhoneCode.objects.get(phone=phone)
        except PhoneCode.DoesNotExist:
            raise serializers.ValidationError({"error": "Код не найден"})

        if phone_code.created_at < timezone.now() - timedelta(minutes=10):
            phone_code.delete()
            raise serializers.ValidationError(
                {"error": "Код просрочен. Запросите новый"}
            )

        if phone_code.attempts >= MAX_ATTEMPTS:
            phone_code.delete()
            raise serializers.ValidationError(
                {"error": "Превышено количество попыток. Код удалён"}
            )

        if code != phone_code.code:
            phone_code.increment_attempts()
            raise serializers.ValidationError({"error": "Неверный код"})

        return attrs

    def save(self):
        phone = self.validated_data["phone"]
        user = User.objects.get(phone=phone)
        user.is_active = True
        user.save()

        PhoneCode.objects.filter(phone=phone).delete()

        return user
