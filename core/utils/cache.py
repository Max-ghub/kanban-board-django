from functools import wraps

from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.response import Response


def _build_cache_key(request):
    return f"response-cache:{request.get_full_path()}"


def _restore_response(payload):
    response = HttpResponse(
        content=payload["content"],
        content_type=payload["content_type"],
        status=payload["status_code"],
    )
    for header, value in payload.get("headers", []):
        if header.lower() == "content-type":
            continue
        response[header] = value
    return response


def cache_response(ttl=60):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(self_or_request, *args, **kwargs):
            request = getattr(self_or_request, "request", self_or_request)

            method = request.method.upper()
            if method != "GET":
                return view_func(self_or_request, *args, **kwargs)

            cache_key = _build_cache_key(request)
            cached_payload = cache.get(cache_key)
            if cached_payload is not None:
                return _restore_response(cached_payload)

            response = view_func(self_or_request, *args, **kwargs)
            if getattr(response, "status_code", None) != 200:
                return response
            if getattr(response, "streaming", False):
                return response

            def store_payload(resp):
                payload = {
                    "headers": list(resp.items()),
                    "content": resp.content,
                    "content_type": resp.get("Content-Type"),
                    "status_code": resp.status_code,
                }
                cache.set(cache_key, payload, ttl)
                return resp

            if isinstance(response, Response):
                response.add_post_render_callback(store_payload)
                return response
            if hasattr(response, "render"):
                response.render()

            return store_payload(response)

        return wrapped

    return decorator
