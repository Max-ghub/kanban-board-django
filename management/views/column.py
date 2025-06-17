from django.db import transaction
from django.db.models import Max
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from management.models import Board, Column
from management.serializes.column import (
    BoardColumnReorderModelSerializer,
    ColumnModelSerializer,
)
from management.services.column import BoardColumnReorderService


class CreateColumnAPIView(generics.CreateAPIView):
    serializer_class = ColumnModelSerializer

    def perform_create(self, serializer):
        board = Board.objects.get(pk=self.kwargs.get("board_id"))
        with transaction.atomic():
            max_order = board.columns.aggregate(Max("order")).get("order__max")
            order = max_order + 1 if max_order is not None else 0
            serializer.save(board=board, order=order)


class UpdateColumnAPIView(generics.UpdateAPIView):
    serializer_class = ColumnModelSerializer
    lookup_url_kwarg = "column_id"

    def get_queryset(self):
        return Column.objects.filter(board_id=self.kwargs.get("board_id"))


class ColumnsReorderAPIView(APIView):
    def post(self, request, board_id: int):
        serializer = BoardColumnReorderModelSerializer(
            data=request.data, context={"board_id": board_id}
        )
        serializer.is_valid(raise_exception=True)

        column_ids = serializer.validated_data.get("column_ids")
        BoardColumnReorderService.reorder(board_id, column_ids)

        return Response(
            {"message": "Порядок колонок обновлён"}, status=status.HTTP_200_OK
        )
