from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from phone.tasks import send_phone_code_task

User = get_user_model()

user_activated = Signal()


@receiver(post_save, sender=User)
def send_phone_code_on_user_created(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        send_phone_code_task.delay(instance.phone)
