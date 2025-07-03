from django.db import models

from .base_model import BaseManagementModel
from .project import Project


class Board(BaseManagementModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="boards"
    )
    title = models.CharField(max_length=64, blank=False)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "management_boards"
        verbose_name = "Доска"
        verbose_name_plural = "Досоки"
