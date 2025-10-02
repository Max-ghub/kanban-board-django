from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import Client

URLS = [
    "/api/v1/users/",
]


class Command(BaseCommand):
    help = "Warm cache"

    def handle(self, *args, **kwargs):
        if "localhost" not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ["localhost"]

        client = Client()
        for url in URLS:
            resp = client.get(
                url,
                HTTP_HOST="localhost",  # явно задаём хост
                HTTP_ACCEPT="application/json",
            )
            self.stdout.write(f"{url}: {resp.status_code}")
