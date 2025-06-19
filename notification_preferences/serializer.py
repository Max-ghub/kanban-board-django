from rest_framework import serializers

from notification_preferences.models import NotificationPreferences


class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreferences
        fields = [
            "email_enabled",
            "sms_enabled",
        ]
        extra_kwargs = {
            "email_enabled": {"required": True},
            "sms_enabled": {"required": True},
        }
