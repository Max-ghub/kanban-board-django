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
        default_version="Alfa",
        description="API для регистрации, аутентификации и работы с пользователями",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", index_page),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("", include("django_prometheus.urls")),
]

# Подключаем Debug Toolbar только в DEBUG и если он установлен
if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns += [
            path("__debug__/", include(debug_toolbar.urls)),
        ]
    except ImportError:
        # В окружении без debug_toolbar (например Celery) пропускаем подключение
        pass
