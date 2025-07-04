from django.urls import path

from users.views.auth import AuthRefreshView, AuthView

urlpatterns = [
    path("", AuthView.as_view(), name="auth"),
    path("refresh/", AuthRefreshView.as_view(), name="auth_refresh"),
]
