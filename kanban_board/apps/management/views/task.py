from rest_framework.viewsets import ModelViewSet

from kanban_board.apps.management.models import Task
from kanban_board.apps.management.serializes.task import TaskModelSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
