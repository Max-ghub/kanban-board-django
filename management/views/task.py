from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
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
    serializer_class = TaskModelSerializer
    permission_classes = [IsAuthenticated, IsProjectMemberOrOwner]

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(
            Q(column__board__project__owner=user)
            | Q(column__board__project__members=user)
        ).distinct()

    def get_object(self):
        queryset = Task.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        obj = get_object_or_404(queryset, **{self.lookup_field: lookup_value})
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        column = serializer.validated_data.get("column")
        parent = serializer.validated_data.get("parent")
        assignee = serializer.validated_data.get("assignee")

        self._validate_relations(column=column, parent=parent, assignee=assignee)

        serializer.save()

    def perform_update(self, serializer):
        validated_data = serializer.validated_data
        column = validated_data.get("column", serializer.instance.column)
        parent = validated_data.get("parent", serializer.instance.parent)
        assignee = validated_data.get("assignee", serializer.instance.assignee)

        self._validate_relations(column=column, parent=parent, assignee=assignee)

        serializer.save()

    def _validate_relations(self, *, column, parent, assignee):
        if column is None:
            raise ValidationError({"column": "Колонка обязательна"})

        project = column.board.project
        if not self._is_user_in_project(self.request.user, project):
            raise ValidationError({"column": "Нет доступа к выбранному проекту"})

        if parent is not None:
            parent_project_id = parent.column.board.project_id
            if parent_project_id != project.id:
                raise ValidationError(
                    {"parent": "Родительская задача должна быть в том же проекте"}
                )

        if assignee is not None and not self._is_user_in_project(assignee, project):
            raise ValidationError(
                {"assignee": "Исполнитель должен быть участником проекта"}
            )

    @staticmethod
    def _is_user_in_project(user, project):
        if user is None:
            return False
        if project.owner_id == user.id:
            return True
        return project.members.filter(pk=user.pk).exists()

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
            data=request.data, context={"parent_task": parent_task, "view": self}
        )
        serializer.is_valid(raise_exception=True)
        self._validate_relations(
            column=parent_task.column,
            parent=parent_task,
            assignee=serializer.validated_data.get("assignee"),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=201)
