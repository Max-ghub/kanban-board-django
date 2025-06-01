import random
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def generate_phone_code():
    """Генерация SMS кода"""
    return str(random.randint(100000, 999999))


class PhoneCode(models.Model):
    """Модель телефонного кода"""

    objects = models.Manager()

    phone = models.CharField(max_length=12, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_phone_code(cls, phone, code):
        """Создание кода"""
        cls.delete_phone_codes(phone)
        cls.objects.create(phone=phone, code=code)

    @classmethod
    def delete_phone_codes(cls, phone):
        """Удаление всех кодов для номера"""
        cls.objects.filter(phone=phone).delete()

    @classmethod
    def verify_phone_code(cls, phone, code):
        """Подтверждение валидности кода"""
        try:
            phone_code = cls.objects.get(phone=phone, code=code)
        except cls.DoesNotExist:
            raise ValidationError("Неверный код")

        if phone_code.created_at < timezone.now() - timedelta(minutes=30):
            raise ValidationError("Код просрочен")

    class Meta:
        db_table = "phone_codes"
