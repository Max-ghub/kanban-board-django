from django.urls import path

from users.views.auth import AuthenticationRefreshView, AuthenticationView

urlpatterns = [
    path("", AuthenticationView.as_view(), name="auth"),
    path("refresh/", AuthenticationRefreshView.as_view(), name="auth_refresh"),
]
