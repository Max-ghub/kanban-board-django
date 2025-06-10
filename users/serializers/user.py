from rest_framework.serializers import ModelSerializer

from users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone",
            "username",
            "name",
            "surname",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["is_active", "date_joined"]
