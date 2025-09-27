from rest_framework import serializers

from management.models import Board, Column


class ColumnModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=64)

    class Meta:
        model = Column
        fields = ["id", "title", "order", "board", "updated_at", "created_at"]
        extra_kwargs = {
            "board": {"read_only": True},
            "order": {"read_only": True},
        }


class BoardColumnReorderModelSerializer(serializers.Serializer):
    board_id = serializers.IntegerField(read_only=True)
    column_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        error_messages={
            "empty": "Список не может быть пустым",
            "not_a_list": "Поле должно содержать список колонок",
        },
    )

    def validate_column_ids(self, new_ids):
        board_id = self.context.get("board_id")
        actual_ids = Column.objects.filter(board_id=board_id).values_list(
            "id", flat=True
        )
        if not actual_ids:
            if Board.objects.filter(pk=board_id).exists():
                raise serializers.ValidationError(
                    "У таблицы нет привязанных к ней колонок"
                )
            raise serializers.ValidationError("Таблица не найдена")

        if len(set(new_ids)) != len(new_ids):
            raise serializers.ValidationError("Список содержит дубликаты")
        if set(new_ids) != set(actual_ids):
            raise serializers.ValidationError("Не соответствует текущим колонкам доски")

        return new_ids
