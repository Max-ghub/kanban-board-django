from rest_framework.exceptions import ValidationError

from management.models import Project
from users.models import User


class ProjectService:
    @staticmethod
    def add_member(project: Project, user: User) -> Project:
        if project.members.filter(pk=user.pk).exists():
            raise ValidationError({"user": "Пользователь уже состоит в проекте"})
        project.members.add(user)
        return project

    @staticmethod
    def delete_member(project: Project, user: User) -> Project:
        if not project.members.filter(pk=user.pk).exists():
            raise ValidationError(
                {"user": "Пользователь не является участником проекта"}
            )
        if user.pk == project.owner_id:
            raise ValidationError({"user": "Пользователь является владельцем"})
        project.members.remove(user)
        return project
