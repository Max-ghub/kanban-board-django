import json

from django.core.exceptions import ValidationError


def parse_request_json_data(request):
    """Получение JSON данных запроса в виде объекта"""
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        raise ValidationError("Невалидный JSON")


def validate_request_json_data(data, required):
    """
    Валидация необходимых полей в запросе.
    required - List, в котором указываются Str поля, которые нужно проверить на наличие
    """
    if not required:
        raise ValidationError("Не были переданы required поля")

    for field in required:
        if field not in data:
            raise ValidationError(f"Отсутствует поле: {field}")
