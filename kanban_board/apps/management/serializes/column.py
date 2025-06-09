from rest_framework.serializers import ModelSerializer

from kanban_board.apps.management.models import Column


class ColumnSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = "__all__"
        read_only_fields = ["board", "order"]


class ColumnReorderSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = ["order"]
