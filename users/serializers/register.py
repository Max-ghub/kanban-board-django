from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from phone.models import CODE_TTL, PhoneCode
from users.services import activate_user_by_phone
from users.validators import phone_validator

User = get_user_model()

MAX_SEND_CODE_ATTEMPTS = 5


class RegisterUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_validator])

    class Meta:
        model = User
        fields = ["phone", "username", "name", "surname", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterVerifyUserSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phone_validator])
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs.get("phone")
        code = attrs.get("code")

        try:
            phone_code = PhoneCode.objects.get(phone=phone)
        except PhoneCode.DoesNotExist:
            raise serializers.ValidationError({"error": "Код не найден"})

        if phone_code.created_at < timezone.now() - CODE_TTL:
            phone_code.delete()
            raise serializers.ValidationError(
                {"error": "Код просрочен. Запросите новый"}
            )

        if phone_code.attempts >= MAX_SEND_CODE_ATTEMPTS:
            phone_code.delete()
            raise serializers.ValidationError(
                {"error": "Превышено количество попыток. Код удалён"}
            )

        if code != phone_code.code:
            phone_code.increment_attempts()
            raise serializers.ValidationError({"error": "Неверный код"})

        return attrs

    def save(self):
        return activate_user_by_phone(self.validated_data["phone"])
