from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.utils.view import get_object_or_404
from kanban_board.apps.management.models import Column, Task
from kanban_board.apps.management.serializes.task import TaskModelSerializer
from users.models import User


def get_request_field(request, field_name):
    value = request.data.get(field_name)
    if not value:
        raise ValidationError(detail={"error": f"{field_name} не указан"})
    return value


def save_serializer(serializer_class, **kwargs):
    serializer = serializer_class(**kwargs)
    if serializer.is_valid():
        serializer.save()
    else:
        raise ValidationError(detail={"error": serializer.errors})


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer

    @action(detail=True, methods=["post"], url_path="move")
    def move_task(self, request, pk=None):
        task = get_object_or_404(model=Task, pk=pk)

        column_id = get_request_field(request=request, field_name="column_id")
        column = get_object_or_404(model=Column, pk=column_id)

        save_serializer(
            serializer_class=TaskModelSerializer,
            instance=task,
            data={"column": column.id},
            partial=True,
        )

        return Response({"message": f"Задача перемещена в колонку {column_id}"})

    @action(detail=True, methods=["post"], url_path="assign")
    def set_assign(self, request, pk=None):
        task = get_object_or_404(model=Task, pk=pk)

        user_id = get_request_field(request=request, field_name="user_id")
        user = get_object_or_404(model=User, pk=user_id)

        save_serializer(
            serializer_class=TaskModelSerializer,
            instance=task,
            data={"assignee": user.id},
            partial=True,
        )

        return Response({"message": f"Установлен исполнитель задачи {user_id}"})

    @action(detail=True, methods=["post"], url_path="subtasks")
    def create_subtask(self, request, pk=None):
        pass
