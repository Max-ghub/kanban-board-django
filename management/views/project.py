from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from management.models import Project
from management.serializes.project import ProjectMemberSerializer, ProjectSerializer
from management.services.project import ProjectMemberService

class ProjectPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 100

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination

    @action(
        detail=True,
        methods=["post"],
        url_path="members",
    )
    def add_member(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated = ProjectMemberService.add_member(
            project, serializer.validated_data["user_id"]
        )

        return Response(ProjectSerializer(updated).data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["delete"],
        url_path="members/(?P<user_id>[^/.]+)",
    )
    def delete_member(self, request, pk=None, user_id=None):
        project = self.get_object()
        serializer = ProjectMemberSerializer(data={"user_id": user_id})
        serializer.is_valid(raise_exception=True)

        updated = ProjectMemberService.delete_member(
            project, serializer.validated_data["user_id"]
        )

        return Response(ProjectSerializer(updated).data, status=status.HTTP_200_OK)
