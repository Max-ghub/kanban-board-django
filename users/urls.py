from django.urls import path

from users.views.auth import AuthRefreshView, AuthView
from users.views.register import RegisterUserView, RegisterVerifyUserView

urlpatterns = [
    # Auth
    path("auth/", AuthView.as_view(), name="auth"),
    path("auth/refresh/", AuthRefreshView.as_view(), name="auth_refresh"),
    # Register
    path("register/", RegisterUserView.as_view(), name="register"),
    path("register/verify/", RegisterVerifyUserView.as_view(), name="register_verify"),
]
