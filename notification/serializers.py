from rest_framework import serializers

from notification.models import Notification, NotificationSettings


class NotificationSerializer(serializers.ModelSerializer):
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


class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ["show_unread_only"]
        extra_kwargs = {"show_unread_only": {"required": True}}
