import requests
from django.core.management.base import BaseCommand

CACHE_WARM_URLS = [
    "http://127.0.0.1:8000/api/users/",
]


class Command(BaseCommand):
    help = "Прогревает кэш для популярных эндпоинтов"

    def handle(self, *args, **kwargs):
        for url in CACHE_WARM_URLS:
            try:
                response = requests.get(url, headers={"Accept": "application/json"})
                self.stdout.write(f"[{response.status_code}]")
            except Exception as e:
                self.stdout.write(f"Ошибка при запросе {url}: {e}")
