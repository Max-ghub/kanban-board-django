from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.models import Notification, NotificationSettings
from notification.serializers import (
    NotificationSerializer,
    NotificationSettingsSerializer,
)


class NotificationView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notification_settings, _ = NotificationSettings.objects.get_or_create(user=user)
        notifications = user.notifications.all()
        if notification_settings.show_unread_only:
            notifications = notifications.filter(is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, notification_id):
        notification = get_object_or_404(
            Notification, pk=notification_id, user=request.user
        )
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationReadView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, notification_id):
        notification = get_object_or_404(
            Notification, pk=notification_id, user=request.user
        )

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        return Response(
            {"status": "read", "id": notification_id}, status=status.HTTP_200_OK
        )


class NotificationSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notification_settings, _ = NotificationSettings.objects.get_or_create(
            user=request.user
        )
        serializer = NotificationSettingsSerializer(notification_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=NotificationSettingsSerializer)
    def put(self, request):
        notification_settings, _ = NotificationSettings.objects.get_or_create(
            user=request.user
        )
        serializer = NotificationSettingsSerializer(
            notification_settings, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
