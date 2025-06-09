from django.db import transaction
from django.db.models import Max
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from kanban_board.apps.management.models import Board, Column
from kanban_board.apps.management.serializes.column import (
    ColumnReorderSerializer,
    ColumnSerializer,
)


class CreateColumnAPIView(generics.CreateAPIView):
    serializer_class = ColumnSerializer

    def perform_create(self, serializer):
        board = Board.objects.get(pk=self.kwargs["board_id"])

        max_order = board.columns.aggregate(Max("order"))["order__max"]
        order = max_order + 1 if max_order is not None else 0

        serializer.save(board=board, order=order)


class UpdateColumnAPIView(generics.UpdateAPIView):
    serializer_class = ColumnSerializer
    lookup_url_kwarg = "column_id"

    def get_queryset(self):
        return Column.objects.filter(board_id=self.kwargs["board_id"])


class ColumnsReorderAPIView(APIView):
    def post(self, request, board_id):
        try:
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return Response(
                data={"error": f"Доска {board_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        column_ids = request.data["column_ids"]
        if not isinstance(column_ids, list):
            return Response({"error": "Поле column_ids должно содержать список"})

        with transaction.atomic():
            for order, column_id in enumerate(column_ids):
                try:
                    column = board.columns.get(pk=column_id)
                except Column.DoesNotExist:
                    transaction.set_rollback(True)
                    return Response(
                        data={column_id: "Колонка не найдена"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                column_serializer = ColumnReorderSerializer(
                    column, data={"order": order}, partial=True
                )
                if not column_serializer.is_valid():
                    transaction.set_rollback(True)
                    return Response(
                        data={column_id: column_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                column_serializer.save()

            return Response(
                data={"message": "Порядок колонок обновлён"}, status=status.HTTP_200_OK
            )
