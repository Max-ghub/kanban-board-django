from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound


def get_object_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        raise NotFound(detail={"error": f"{model.__name__} не найдено"})


def ensure_object_exists_or_404(model, error_message=None, **kwargs):
    if not model.objects.filter(**kwargs).exists():
        msg = error_message or {"error": f"{model.__name__} не найдено"}
        raise NotFound(detail=msg)
