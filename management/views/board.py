from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.utils.cache import cache_response
from management.models import Board
from management.premissions import IsProjectMemberOrOwner
from management.serializes.board import BoardModelSerializer


@method_decorator(cache_response(ttl=60), name="list")
class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardModelSerializer
    permission_classes = [IsAuthenticated, IsProjectMemberOrOwner]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(project__owner=user) | Q(project__members=user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        user = self.request.user

        if project.owner != user and not project.members.filter(pk=user.pk).exists():
            raise PermissionDenied(
                "Недостаточно прав, чтобы добавлять доску в этот проект."
            )

        serializer.save()
