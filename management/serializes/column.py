from rest_framework import serializers

from management.models import Column


class ColumnModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128)

    class Meta:
        model = Column
        fields = ["id", "title", "order", "board", "updated_at", "created_at"]
        extra_kwargs = {
            "board": {"read_only": True},
            "order": {"read_only": True},
        }


class BoardColumnReorderModelSerializer(serializers.Serializer):
    column_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        error_messages={
            "not_a_list": "Поле должно содержать список колонок",
            "empty": "Список не может быть пустым",
        },
    )

    def validate_column_ids(self, new_ids):
        board_id = self.context.get("board_id")
        actual_ids = Column.objects.filter(board_id=board_id).values_list(
            "id", flat=True
        )

        if len(set(new_ids)) != len(new_ids):
            raise serializers.ValidationError("Список содержит дубликаты")
        if set(new_ids) != set(actual_ids):
            raise serializers.ValidationError("Не соответствует текущим колонкам доски")

        return new_ids
