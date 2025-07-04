from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404

from phone.models import PhoneCode

User = get_user_model()


def activate_user_by_phone(phone: str) -> User:
    user = get_object_or_404(User, phone=phone)
    user.is_active = True
    user.save()
    PhoneCode.objects.filter(phone=phone).delete()
    return user
