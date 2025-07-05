from datetime import timedelta

from django.db import models

CODE_TTL = timedelta(minutes=10)


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

    def increment_attempts(self):
        self.attempts += 1
        self.save()

    class Meta:
        db_table = "phone_codes"
        verbose_name = "Телефонный код"
        verbose_name_plural = "Телефонные коды"
