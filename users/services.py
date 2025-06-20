from django.contrib.auth import get_user_model

from phone.models import PhoneCode

User = get_user_model()


def activate_user_by_phone(phone: str) -> User:
    user = User.objects.get(phone=phone)
    user.is_active = True
    user.save()
    PhoneCode.objects.filter(phone=phone).delete()
    return user
