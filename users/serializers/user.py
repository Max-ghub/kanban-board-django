from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
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
        extra_kwargs = {
            "is_active": {"read_only": True},
            "date_joined": {"read_only": True},
        }
