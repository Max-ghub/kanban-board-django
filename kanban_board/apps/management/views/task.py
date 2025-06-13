from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.utils.view import ensure_object_exists_or_404, get_object_or_404
from kanban_board.apps.management.models import Column, Task
from kanban_board.apps.management.serializes.task import TaskModelSerializer
from users.models import User


def get_request_field(request, field_name, required=True):
    value = request.data.get(field_name)
    if required and value is None:
        raise ValidationError(detail={field_name: "обязательное поле"})
    return value


def validate_and_save_serializer(
    serializer_class, *, instance=None, data=None, partial=True
):
    serializer = serializer_class(instance=instance, data=data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer

    @action(detail=True, methods=["post"], url_path="move")
    def move_task(self, request, pk=None):
        task = self.get_object()
        column_id = get_request_field(request=request, field_name="column_id")
        column = get_object_or_404(Column, pk=column_id)

        serializer = validate_and_save_serializer(
            serializer_class=self.serializer_class,
            instance=task,
            data={"column": column_id},
        )

        Task.objects.filter(parent=task).update(column=column.id)

        return Response(data=serializer.data, status=200)

    @action(detail=True, methods=["post"], url_path="assign")
    def set_assign(self, request, pk=None):
        task = self.get_object()

        user_id = get_request_field(
            request=request, field_name="user_id", required=False
        )
        if user_id is not None:
            ensure_object_exists_or_404(User, pk=user_id)

        serializer = validate_and_save_serializer(
            serializer_class=self.serializer_class,
            instance=task,
            data={"assignee": user_id},
        )

        return Response(data=serializer.data, status=200)

    @action(detail=True, methods=["post"], url_path="subtasks")
    def create_subtask(self, request, pk=None):
        parent_task = self.get_object()
        subtask_data = request.data
        subtask_data["parent"] = parent_task.id
        subtask_data["column"] = parent_task.column.id

        serializer = validate_and_save_serializer(
            serializer_class=self.serializer_class,
            data=subtask_data,
            partial=False,
        )

        return Response(data=serializer.data, status=201)
