from rest_framework.exceptions import NotFound


def ensure_object_exists_or_404(model, error_message=None, **kwargs):
    if not model.objects.filter(**kwargs).exists():
        msg = error_message or {"error": f"{model.__name__} не найдено"}
        raise NotFound(detail=msg)
