from django.http import HttpResponse
from extra_settings.models import Setting


class MaintenanceModeMiddleware:
    def __init__(self, get_response ):
        self.get_response = get_response

    def __call__(self, request):
        if Setting.get("MAINTENANCE_MODE", False):
            return HttpResponse("Идут технические работы")
        return self.get_response(request)