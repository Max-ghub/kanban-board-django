from django.urls import path

from notification.views import (
    NotificationReadView,
    NotificationSettingsView,
    NotificationView,
)

urlpatterns = [
    path("", NotificationView.as_view()),
    path("<int:notification_id>/", NotificationView.as_view()),
    path("<int:notification_id>/read/", NotificationReadView.as_view()),
    path("settings/", NotificationSettingsView.as_view()),
]
