from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import index_page

schema_view = get_schema_view(
    openapi.Info(
        title="Kanban API",
        default_version="v1",
        description="API для регистрации, аутентификации, работы с пользователями и канбан доской",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", index_page),
    path("api/", include("api.urls")),
    path("", include("users.urls")),
    path("admin/", admin.site.urls),
]
# Swagger
urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
# Prometheus
urlpatterns += [
    path("", include("django_prometheus.urls")),
]

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
