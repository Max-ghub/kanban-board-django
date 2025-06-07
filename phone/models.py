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

    phone = models.CharField(max_length=12, unique=True)
    code = models.CharField(max_length=6)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    @classmethod
    def create_phone_code(cls, phone, code):
        """Создание кода"""
        cls.objects.filter(phone=phone).delete()
        cls.objects.create(phone=phone, code=code)

    @classmethod
    def verify_phone_code(cls, phone, code):
        """Подтверждение валидности кода"""
        try:
            phone_code = cls.objects.get(phone=phone, code=code)
        except cls.DoesNotExist:  # type: ignore[attr-defined]
            raise ValidationError("Введён неверный код")

        if phone_code.created_at < timezone.now() - timedelta(minutes=1):
            cls.objects.filter(phone=phone).delete()
            raise ValidationError("Код просрочен. Попробуйте зарегистрироваться заново")

        cls.objects.filter(phone=phone).delete()

    def increment_attempts(self):
        self.attempts += 1
        self.save()

    class Meta:
        db_table = "phone_codes"
