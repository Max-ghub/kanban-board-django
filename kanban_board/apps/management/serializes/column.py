from rest_framework.serializers import ModelSerializer

from kanban_board.apps.management.models import Column


class ColumnModelSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = "__all__"
        extra_kwargs = {
            "board": {"read_only": True},
            "order": {"read_only": True},
        }


class ColumnReorderModelSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = ["order"]
