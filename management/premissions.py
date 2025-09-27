from rest_framework.permissions import SAFE_METHODS, BasePermission


def _resolve_project(obj):
    if hasattr(obj, "owner"):
        return obj
    elif hasattr(obj, "project"):
        return obj.project
    elif hasattr(obj, "board"):
        return obj.board.project
    elif hasattr(obj, "column"):
        return obj.column.board.project
    else:
        return None


class IsProjectMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = _resolve_project(obj)
        if project is None:
            return False

        user = request.user
        if project.owner == user:
            return True
        elif project.members.filter(pk=user.pk).exists():
            return request.method in SAFE_METHODS

        return False


class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = _resolve_project(obj)
        if project is None:
            return False

        user = request.user
        return project.owner == user


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = _resolve_project(obj)
        if project is None:
            return False

        user = request.user
        if not user.is_authenticated:
            return False

        if project.owner_id == user.pk:
            return True

        return project.members.filter(pk=user.pk).exists()
