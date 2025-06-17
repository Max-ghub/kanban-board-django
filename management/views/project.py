from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from management.models import Project
from management.serializes.project import ProjectMemberSerializer, ProjectSerializer
from management.services.project import ProjectMemberService


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(
        detail=True,
        methods=["post"],
        url_path="members",
        serializer_class=ProjectMemberSerializer,
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
        serializer_class=ProjectMemberSerializer,
    )
    def delete_member(self, request, pk=None, user_id=None):
        project = self.get_object()
        serializer = ProjectMemberSerializer(data={"user_id": user_id})
        serializer.is_valid(raise_exception=True)

        updated = ProjectMemberService.delete_member(
            project, serializer.validated_data["user_id"]
        )

        return Response(ProjectSerializer(updated).data, status=status.HTTP_200_OK)
