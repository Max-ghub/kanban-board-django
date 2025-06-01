from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.utils.jwt import generate_tokens
from core.utils.request import parse_request_json_data, validate_request_json_data
from phone.models import PhoneCode
from users.utils import validation_new_user

User = get_user_model()


@csrf_exempt
@require_POST
def registration_view(request):
    """Регистрация пользователя"""
    data = parse_request_json_data(request)

    required = ["phone", "username", "password"]
    validate_request_json_data(data, required)

    phone = data.pop("phone")
    username = data.pop("username")
    password = data.pop("password")
    extra_fields = data
    validation_new_user(phone, username)

    User.objects.create_user(
        phone=phone, username=username, password=password, **extra_fields
    )

    return JsonResponse(
        {
            "message": f"На телефон {phone} был отправлен код для подтверждения регистрации"
        }
    )


@csrf_exempt
@require_POST
def confirm_registration_view(request):
    """Подтверждение регистрации пользователя"""
    data = parse_request_json_data(request)
    required = ["phone", "code"]
    validate_request_json_data(data, required)

    phone = data["phone"]
    code = data["code"]

    PhoneCode.verify_phone_code(phone, code)
    PhoneCode.delete_phone_codes(phone)

    user = User.objects.get(phone=phone)
    user.is_active = True
    user.save()

    token = generate_tokens(user)
    return JsonResponse(token)
