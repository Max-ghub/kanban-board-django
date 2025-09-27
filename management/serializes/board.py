from django.db.models import Q
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from management.models import Board
from management.models.project import Project


class BoardModelSerializer(ModelSerializer):
    project = PrimaryKeyRelatedField(queryset=Project.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request is None:
            return

        user = request.user
        user_projects = Project.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()
        self.fields["project"].queryset = user_projects

    class Meta:
        model = Board
        fields = ["id", "title", "project", "updated_at", "created_at"]
        read_only_fields = ["id"]
