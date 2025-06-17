from rest_framework.viewsets import ModelViewSet

from management.models import Board
from management.serializes.board import BoardModelSerializer


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardModelSerializer
