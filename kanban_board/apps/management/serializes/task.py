from rest_framework.serializers import ModelSerializer

from kanban_board.apps.management.models import Task


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
