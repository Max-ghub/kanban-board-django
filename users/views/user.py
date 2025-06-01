from django.http import HttpResponse, JsonResponse

from users.models import User


def get_user_view(request, user_id):
    """Получение user по его id"""
    try:
        return HttpResponse(User.objects.get(id=user_id))
    except User.DoesNotExist:
        return JsonResponse({"error": "Пользователь не сущетствует"})
