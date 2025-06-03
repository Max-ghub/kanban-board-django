from django.urls import path

from .views.project import ProjectView

urlpatterns = [
    path("api/projects/", ProjectView.as_view()),
    path("api/projects/<int:project_id>/", ProjectView.as_view()),
]
