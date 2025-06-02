from django.db import models

from .task import Task


class RelationTaskType(models.TextChoices):
    BLOCKS = "blocks", "Blocks"
    DEPENDS_ON = "depends_on", "Depends_on"
    DUPLICATE = "duplicate", "Duplicate"


class RelationTask(models.Model):
    from_task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="outgoing_relations"
    )
    to_task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="incoming_relations"
    )
    relation_type = models.CharField(max_length=20, choices=RelationTaskType.choices)

    class Meta:
        db_table = "management_relation_tasks"
        unique_together = ("from_task", "to_task", "relation_type")
