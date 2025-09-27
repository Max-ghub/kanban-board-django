from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from management.models import Task
from management.premissions import IsProjectMemberOrOwner, IsProjectOwner
from management.serializes.task import (
    TaskAssigneeSerializer,
    TaskModelSerializer,
    TaskMoveSerializer,
    TaskSubtaskSerializer,
)
from management.services.task import TaskService


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    permission_classes = [IsAuthenticated, IsProjectMemberOrOwner]

    @action(
        detail=True,
        methods=["post"],
        url_path="move",
        permission_classes=[IsProjectOwner],
    )
    def move_task(self, request, pk=None):
        task = self.get_object()
        serializer = TaskMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        column_id = serializer.validated_data.get("column_id")

        TaskService.move_task(task, column_id)

        return Response(data={"message": "Задача перемещена"}, status=200)

    @action(
        detail=True,
        methods=["post"],
        url_path="assign",
        permission_classes=[IsProjectOwner],
    )
    def set_assignee(self, request, pk=None):
        task = self.get_object()
        serializer = TaskAssigneeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get("user_id")

        TaskService.set_assignee(task, user_id)

        message = (
            "Исполнитель назначен" if task.assignee is not None else "Исполнитель убран"
        )
        return Response(data={"message": message}, status=200)

    @action(
        detail=True,
        methods=["post"],
        url_path="subtasks",
        permission_classes=[IsProjectOwner],
    )
    def create_subtask(self, request, pk=None):
        parent_task = self.get_object()

        serializer = TaskSubtaskSerializer(
            data=request.data, context={"parent_task": parent_task}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=201)
