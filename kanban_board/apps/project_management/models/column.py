from django.db import models

from .base_model import BaseManagementModel
from .board import Board


class Column(BaseManagementModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    title = models.CharField(max_length=128, blank=False)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "management_columns"
