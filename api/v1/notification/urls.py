from django.urls import path

from notification.views import (
    NotificationReadView,
    NotificationSettingsView,
    NotificationView,
)

urlpatterns = [
    path("notifications/", NotificationView.as_view()),
    path("notifications/<int:notification_id>/", NotificationView.as_view()),
    path("notifications/<int:notification_id>/read/", NotificationReadView.as_view()),
    path("notifications/settings/", NotificationSettingsView.as_view()),
]
