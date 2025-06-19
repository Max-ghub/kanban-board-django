from rest_framework import serializers

from notification.models import Notification


class NotificationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "message",
            "type",
            "url",
            "is_read",
            "updated_at",
            "created_at",
        ]
