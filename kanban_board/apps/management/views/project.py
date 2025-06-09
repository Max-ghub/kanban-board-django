from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kanban_board.apps.management.models import Project
from kanban_board.apps.management.serializes.project import ProjectSerializer
from users.models import User


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["post"], url_path="members")
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                data={"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        project.members.add(user)
        return Response({"message": f'Участник "{user.username}" добавлен в проект'})

    @action(detail=True, methods=["delete"], url_path="members/(?P<user_id>[^/.]+)")
    def delete_member(self, request, pk=None, user_id=None):
        project = self.get_object()

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                data={"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        project.members.remove(user)
        return Response({"message": f'Участник "{user.username}" удалён из проекта'})
