from django.urls import include, path

urlpatterns = [
    path("", include("api.management.project.urls")),
    path("", include("api.management.board.urls")),
    path("", include("api.management.column.urls")),
    path("", include("api.management.task.urls")),
    # path("", include("api.management.relation_task.urls")),
]
