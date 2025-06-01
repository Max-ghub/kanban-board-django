from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views.authentication import authentication_view
from users.views.registration import confirm_registration_view, registration_view
from users.views.user import get_user_view

urlpatterns = [
    path("api/users/<int:user_id>/", get_user_view),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register", registration_view),
    path("api/register-confirm", confirm_registration_view),
    path("api/auth", authentication_view),
]
