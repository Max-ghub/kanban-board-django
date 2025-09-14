from rest_framework import serializers

from management.models import Project
from users.models import User


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
        extra_kwargs = {
            "owner": {"read_only": True},
            "members": {"read_only": True},
        }


class ProjectMemberSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
