from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from management.models import Board
from management.premissions import IsProjectMemberOrOwner
from management.serializes.board import BoardModelSerializer


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardModelSerializer
    permission_classes = [IsAuthenticated, IsProjectMemberOrOwner]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(project__owner=user) | Q(project__members=user)
        ).distinct()
