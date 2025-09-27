from django.urls import path

from notification_preferences.views import NotificationPreferencesView

urlpatterns = [
    path("notification-preferences/", NotificationPreferencesView.as_view()),
]
