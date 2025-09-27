from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from notification_preferences.models import NotificationPreferences
from notification_preferences.serializer import NotificationPreferencesSerializer


class NotificationPreferencesView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationPreferencesSerializer

    def get_object(self):
        notification_preferences, _ = NotificationPreferences.objects.get_or_create(
            user=self.request.user
        )
        return notification_preferences
