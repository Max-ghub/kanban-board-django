from rest_framework import serializers

from management.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "owner",
            "members",
            "is_archived",
            "updated_at",
            "created_at",
        ]
        extra_kwargs = {"members": {"read_only": True}}


class ProjectMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
