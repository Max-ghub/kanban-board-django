from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification_preferences.models import NotificationPreferences
from notification_preferences.serializer import NotificationPreferencesSerializer


class NotificationPreferencesView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notification_preference = NotificationPreferences.objects.get(user=request.user)
        serializer = NotificationPreferencesSerializer(notification_preference)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        notification_preference = NotificationPreferences.objects.get(user=request.user)
        serializer = NotificationPreferencesSerializer(
            notification_preference, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
