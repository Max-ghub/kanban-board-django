from rest_framework.serializers import ModelSerializer

from management.models import Board


class BoardModelSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ["title", "project", "updated_at", "created_at"]
