from django.dispatch import receiver

from notification_preferences.models import NotificationPreferences
from users.signals import user_activated


@receiver(user_activated)
def create_notification_preferences_settings_on_user_activated(sender, user, **kwargs):
    NotificationPreferences.objects.get_or_create(user=user)
