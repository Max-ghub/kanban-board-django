import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanban_board.settings.main")
app = Celery("kanban")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
