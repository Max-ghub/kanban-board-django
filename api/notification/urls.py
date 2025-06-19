from django.urls import path

from notification.views import (
    NotificationDestroyView,
    NotificationListView,
    NotificationReadView,
)

urlpatterns = [
    path("", NotificationListView.as_view()),
    path("<int:notification_id>/", NotificationDestroyView.as_view()),
    path("<int:notification_id>/read/", NotificationReadView.as_view()),
]
