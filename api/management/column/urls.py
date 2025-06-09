from django.urls import path

from kanban_board.apps.management.views.column import (
    ColumnsReorderAPIView,
    CreateColumnAPIView,
    UpdateColumnAPIView,
)

urlpatterns = [
    path(
        "boards/<int:board_id>/columns/",
        CreateColumnAPIView.as_view(),
        name="column-create",
    ),
    path(
        "boards/<int:board_id>/columns/<int:column_id>/",
        UpdateColumnAPIView.as_view(),
        name="column-update",
    ),
    path(
        "boards/<int:board_id>/columns/reorder/",
        ColumnsReorderAPIView.as_view(),
        name="column-reorder",
    ),
]
