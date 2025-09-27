from django.urls import include, path

urlpatterns = [
    path("", include("api.v1.management.project.urls")),
    path("", include("api.v1.management.board.urls")),
    path("", include("api.v1.management.column.urls")),
    path("", include("api.v1.management.task.urls")),
    # path("", include("api.v1.management.relation_task.urls")),
]
