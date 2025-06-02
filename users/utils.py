from django.core.exceptions import ValidationError

from users.models import User


def validation_new_user(phone, username):
    """Валидация нового пользователя"""
    if User.objects.filter(phone=phone).exists():
        raise ValidationError("Пользователей с таким номером телефона уже существует")
    if User.objects.filter(username=username).exists():
        raise ValidationError("Пользователь с таким логином уже существует")
