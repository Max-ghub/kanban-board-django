from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound


def get_object_or_404(model, error_message=None, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        msg = error_message or {"error": f"{model.__name__} не найден"}
        raise NotFound(detail=msg)
