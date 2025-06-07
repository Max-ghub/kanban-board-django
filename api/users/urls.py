from django.urls import path

from users.views.user import get_user_view

urlpatterns = [path("<int:user_id>/", get_user_view)]
