from rest_framework.serializers import ModelSerializer

from kanban_board.apps.management.models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
