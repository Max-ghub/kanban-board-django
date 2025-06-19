from django.apps import AppConfig


class NotificationPreferencesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notification_preferences"

    def ready(self):
        import notification_preferences.signals
