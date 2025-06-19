from django.urls import path

from notification_preferences.views import NotificationPreferencesView

urlpatterns = [
    path("", NotificationPreferencesView.as_view()),
]
