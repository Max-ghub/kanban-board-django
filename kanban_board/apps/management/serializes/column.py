from rest_framework.serializers import ModelSerializer

from kanban_board.apps.management.models import Column


class ColumnModelSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = "__all__"
        read_only_fields = ["board", "order"]


class ColumnReorderModelSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = ["order"]
