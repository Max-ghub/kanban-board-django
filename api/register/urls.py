from django.urls import path

from users.views.register import RegisterUserView, RegisterVerifyUserView

urlpatterns = [
    path("", RegisterUserView.as_view(), name="register"),
    path("verify/", RegisterVerifyUserView.as_view(), name="register_verify"),
]
