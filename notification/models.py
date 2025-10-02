from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.db.models import Q


class NotificationSettings(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="notification_settings"
    )
    show_unread_only = models.BooleanField(
        default=False,
        verbose_name="Только непрочитанные",
        help_text="Скрывать прочитанные уведомления",
    )

    class Meta:
        db_table = "notifications_settings"
        verbose_name = "Настройка уведомлений"
        verbose_name_plural = "Настройки уведомлений"

    objects = models.Manager()

    def __str__(self):
        return f"Настройки уведомлений для {self.user}"


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        MESSAGE = "MESSAGE", "Новое сообщение в проекте"
        PROJECT_INVITE = "PROJECT_INVITE", "Приглашение в проект: {}"
        TASK_ASSIGNED = "TASK_ASSIGNED", "Вам назначена задача: {}"

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(
        max_length=64,
        blank=True,
        help_text="Краткий заголовок уведомления (автозаполняется из типа уведомления)",
    )
    message = models.TextField(max_length=2048, help_text="Основной текст уведомления")
    is_read = models.BooleanField(default=False, help_text="Прочитано ли уведомление")
    type = models.CharField(
        max_length=32,
        choices=NotificationType.choices,
        default=NotificationType.MESSAGE,
    )
    url = models.URLField(
        blank=True, null=True, help_text="Ссылка для перехода при клике"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        indexes = [
            BrinIndex(fields=["created_at"], name="idx_notification_created_brin"),
            models.Index(
                fields=["user", "created_at"], name="idx_notification_user_created"
            ),
            models.Index(
                fields=["user", "created_at"],
                name="idx_notification_unread",
                condition=Q(is_read=False),
            ),
        ]

    objects = models.Manager()

    def __str__(self):
        return f"Уведомление для {self.user}: {self.title}"
