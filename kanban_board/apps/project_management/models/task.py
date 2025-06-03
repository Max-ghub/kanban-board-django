from django.db import models

from users.models import User

from .base_model import BaseManagementModel
from .column import Column


class TaskStatus(models.TextChoices):
    BACKLOG = "backlog", "Backlog"
    TODO = "todo", "Todo"
    IN_PROGRESS = "in_progress", "In progress"
    REVIEW = "review", "Review"
    DONE = "done", "Done"
    ARCHIVED = "archived", "Archived"


class TaskPriority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


class Task(BaseManagementModel):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=128, blank=False)
    description = models.TextField(max_length=4096, blank=True, null=True)
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20, choices=TaskStatus, default=TaskStatus.BACKLOG
    )
    priority = models.CharField(
        max_length=10, choices=TaskPriority, default=TaskPriority.MEDIUM
    )
    estimated_time = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    actual_time = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "management_tasks"
