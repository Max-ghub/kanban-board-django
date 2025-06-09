from rest_framework import serializers

from kanban_board.apps.management.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
