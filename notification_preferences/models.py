from django.db import models


class NotificationPreferences(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="notification_preferences"
    )
    email_enabled = models.BooleanField(
        default=True, help_text="Получать уведомления на email"
    )
    sms_enabled = models.BooleanField(
        default=False, help_text="Получать уведомления по SMS"
    )

    class Meta:
        db_table = "notification_preferences"
        verbose_name = "Внешняя настройка уведомлений"
        verbose_name_plural = "Внешние настройки уведомлений"

    objects = models.Manager()

    def __str__(self):
        return f"Настройки каналов уведомлений для {self.user}"
