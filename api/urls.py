from django.urls import include, path

urlpatterns = [
    path("register/", include("api.register.urls")),
    path("auth/", include("api.auth.urls")),
    path("users/", include("api.users.urls")),
    path("", include("api.management.urls")),
]
