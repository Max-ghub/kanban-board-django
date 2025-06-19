from rest_framework import generics, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification.models import Notification
from notification.serializers import NotificationModelSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user=self.request.user)

        if user.notification_settings.show_unread_only:
            queryset = queryset.filter(is_read=False)

        return queryset


class NotificationDestroyView(generics.DestroyAPIView):
    serializer_class = NotificationModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "notification_id"
    queryset = Notification.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


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
