from django.http import HttpResponse
from extra_settings.models import Setting
from rest_framework import status


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if Setting.get("MAINTENANCE_MODE", False):
            if not request.path.startswith("/admin/") or request.path.startswith(
                "/static/"
            ):
                return HttpResponse(
                    "Идут технические работы",
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
        return self.get_response(request)
