from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.utils.jwt import generate_tokens
from core.utils.request import parse_request_json_data, validate_request_json_data

User = get_user_model()


@csrf_exempt
@require_POST
def authentication_view(request):
    """Аутентификация пользователя"""
    data = parse_request_json_data(request)
    required = ["phone", "password"]
    validate_request_json_data(data, required)

    phone = data["phone"]
    password = data["password"]

    try:
        user = User.objects.get(phone=phone)
        if not user.check_password(password):
            raise User.DoesNotExist
    except User.DoesNotExist:
        return JsonResponse({"error": "Введён неверный логин или пароль"}, status=400)

    token = generate_tokens(user)
    return JsonResponse(token)
