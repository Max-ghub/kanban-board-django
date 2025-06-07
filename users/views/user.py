from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from users.models import User


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_view(request, user_id):
    """Получение user по его id"""
    try:
        return HttpResponse(User.objects.get(id=user_id))
    except User.DoesNotExist:
        return JsonResponse({"error": "Пользователь не сущетствует"})
