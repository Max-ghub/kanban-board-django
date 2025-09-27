from django.urls import include, path

urlpatterns = [
    path("", include("users.urls_api")),
    path("", include("api.v1.management.urls")),
    path("notifications/", include("api.v1.notification.urls")),
    path("notification-preferences/", include("api.v1.notification_preferences.urls")),
]
