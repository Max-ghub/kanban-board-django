from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kanban_board.apps.management.models import Column, Task
from kanban_board.apps.management.serializes.task import TaskModelSerializer
from users.models import User


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer

    @action(detail=True, methods=["post"], url_path="move")
    def move_task(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                data={"error": f"Задача {pk} не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        column_id = request.data.get("column_id")
        if not column_id:
            return Response(
                data={"error": "column_id не указан"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            column = Column.objects.get(pk=column_id)
        except Column.DoesNotExist:
            return Response(
                data={"error": f"Колонка {column_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task_serializer = TaskModelSerializer(
            task, data={"column": column.id}, partial=True
        )
        if task_serializer.is_valid():
            task_serializer.save()
        else:
            return Response(
                {"error": task_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": f"Задача перемещена в колонку {column_id}"})

    @action(detail=True, methods=["post"], url_path="assign")
    def set_assign(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                data={"error": f"Задача {pk} не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                data={"error": "user_id не указан"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                data={"error": f"Пользователь {user_id} не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task_serializer = TaskModelSerializer(task, {"assignee": user.id}, partial=True)
        if task_serializer.is_valid():
            task_serializer.save()
        else:
            return Response(
                {"error": task_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": f"Установлен исполнитель задачи {user_id}"})

    @action(detail=True, methods=["post"], url_path="subtasks")
    def create_subtask(self, request, pk=None):
        pass
