from management.models import Column


class BoardColumnReorderService:
    @staticmethod
    def reorder(board_id: int, column_ids: list[int]) -> None:
        columns = Column.objects.filter(board_id=board_id)
        column_map = {column.id: column for column in columns}

        for order, column_id in enumerate(column_ids):
            column = column_map[column_id]
            column.order = order

        Column.objects.bulk_update(column_map.values(), ["order"])
