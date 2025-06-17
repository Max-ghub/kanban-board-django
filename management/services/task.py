from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from management.models import Column, Task
from users.models import User


class TaskService:
    @staticmethod
    def move_task(task: Task, column_id: int) -> None:
        column = get_object_or_404(Column, pk=column_id)

        if task.column.board_id != column.board_id:
            raise ValidationError({"column_id": "Колонка должна быть в той же доске"})
        if task.column.id == column_id:
            raise ValidationError({"column_id": "Задача уже в этой колонке"})

        task.column = column
        task.save()

    @staticmethod
    def set_assignee(task, user_id):
        user = get_object_or_404(User, pk=user_id) if user_id is not None else None

        if task.assignee_id == user_id:
            raise ValidationError({"user_id": "Назначение не изменяет исполнителя"})

        task.assignee = user
        task.save()
