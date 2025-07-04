from django.dispatch import receiver

from notification.models import NotificationSettings
from users.signals import user_activated


@receiver(user_activated)
def create_notification_settings_on_user_activated(sender, user, **kwargs):
    NotificationSettings.objects.get_or_create(user=user)
