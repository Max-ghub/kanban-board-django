from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from kanban_board.apps.management.models import Project
from users.models import User


class ProjectMemberService:
    @staticmethod
    def add_member(project: Project, user_id: int) -> Project:
        user = get_object_or_404(User, pk=user_id)
        if project.members.filter(pk=user.pk).exists():
            raise ValidationError({"user_id": "Пользователь уже состоит в проекте"})
        project.members.add(user)
        return project

    @staticmethod
    def delete_member(project: Project, user_id: int) -> Project:
        user = get_object_or_404(User, pk=user_id)
        if not project.members.filter(pk=user.pk).exists():
            raise ValidationError(
                {"user_id": "Пользователь не является участником проекта"}
            )
        if user.pk == project.owner_id:
            raise ValidationError({"user_id": "Пользователь является владельцем"})
        project.members.remove(user)
        return project
