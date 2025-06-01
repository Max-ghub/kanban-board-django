from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import index_page

schema_view = get_schema_view(
    openapi.Info(
        title="Kanban API",
        default_version="Alfa",
        description="API для регистрации, аутентификации и работы с пользователями",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", index_page),
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
] + debug_toolbar_urls()
