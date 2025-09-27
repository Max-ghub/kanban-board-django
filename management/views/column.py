from django.db import transaction
from django.db.models import Max, Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.models import Board, Column
from management.premissions import IsProjectMember
from management.serializes.column import (
    BoardColumnReorderModelSerializer,
    ColumnModelSerializer,
)
from management.services.column import BoardColumnReorderService


def _get_board_for_user_or_403(user, board_id: int) -> Board:
    accessible_boards = Board.objects.filter(
        Q(project__owner=user) | Q(project__members=user)
    ).distinct()

    try:
        return get_object_or_404(accessible_boards, pk=board_id)
    except Http404 as exc:
        if Board.objects.filter(pk=board_id).exists():
            raise PermissionDenied("Недостаточно прав для доступа к доске") from exc
        raise


class CreateColumnAPIView(generics.CreateAPIView):
    serializer_class = ColumnModelSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def perform_create(self, serializer):
        board_id = self.kwargs.get("board_id")
        board = _get_board_for_user_or_403(self.request.user, board_id)
        self.check_object_permissions(self.request, board)
        with transaction.atomic():
            max_order = board.columns.aggregate(Max("order")).get("order__max")
            order = max_order + 1 if max_order is not None else 0
            serializer.save(board=board, order=order)


class UpdateColumnAPIView(generics.UpdateAPIView):
    serializer_class = ColumnModelSerializer
    lookup_url_kwarg = "column_id"
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        return Column.objects.filter(board_id=self.kwargs.get("board_id"))


class ColumnsReorderAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectMember]

    def post(self, request, board_id: int):
        board = _get_board_for_user_or_403(request.user, board_id)
        self.check_object_permissions(request, board)
        serializer = BoardColumnReorderModelSerializer(
            data=request.data, context={"board_id": board_id}
        )
        serializer.is_valid(raise_exception=True)

        column_ids = serializer.validated_data.get("column_ids")
        BoardColumnReorderService.reorder(board_id, column_ids)

        return Response(
            {"message": "Порядок колонок обновлён"}, status=status.HTTP_200_OK
        )
