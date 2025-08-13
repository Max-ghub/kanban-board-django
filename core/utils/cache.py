import json
from functools import wraps

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response


def cache_response(timeout=60):
    """
    Кэширует JSON-ответ в Redis для GET-запросов.
    Работает с DRF ViewSet/APIView и обычными CBV/FBV.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self_or_request, *args, **kwargs):
            request = getattr(self_or_request, "request", self_or_request)

            if request.method != "GET":
                return view_func(self_or_request, *args, **kwargs)

            cache_key = f"{request.get_full_path()}:{request.method}"

            cached = cache.get(cache_key)
            if cached is not None:
                return Response(cached, status=status.HTTP_200_OK)

            response = view_func(self_or_request, *args, **kwargs)

            if getattr(response, "status_code", None) == 200:
                try:
                    if hasattr(response, "data"):
                        payload = response.data  # DRF Response
                    else:
                        payload = json.loads(response.content)  # HttpResponse
                    cache.set(cache_key, payload, timeout=timeout)
                except Exception:
                    pass

            return response

        return _wrapped_view

    return decorator
