from django.db import models

from .base_model import BaseManagementModel
from .board import Board


class Column(BaseManagementModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    title = models.CharField(max_length=64, blank=False)
    order = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "management_columns"
        verbose_name = "Колонка"
        verbose_name_plural = "Колонки"
        ordering = ["order"]
        indexes = [
            models.Index(fields=["board", "order"], name="idx_column_board_order"),
        ]
