from rest_framework.viewsets import ModelViewSet

from kanban_board.apps.management.models import Board
from kanban_board.apps.management.serializes.board import BoardSerializer


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
