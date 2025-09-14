from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from management.models import Project
from management.premissions import IsProjectMemberOrOwner, IsProjectOwner
from management.serializes.project import ProjectMemberSerializer, ProjectSerializer
from management.services.project import ProjectService


class ProjectPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        with transaction.atomic():
            project = serializer.save(owner=self.request.user)
            project.members.add(self.request.user)

    def get_permissions(self):
        if self.action in ["create", "list"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsProjectMemberOrOwner()]

    @action(
        detail=True,
        methods=["post"],
        url_path="members",
        permission_classes=[IsAuthenticated, IsProjectOwner],
    )
    def add_member(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated = ProjectService.add_member(project, serializer.validated_data["user"])

        return Response(ProjectSerializer(updated).data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["delete"],
        url_path="members/(?P<user_id>[^/.]+)",
        permission_classes=[IsAuthenticated, IsProjectOwner],
    )
    def delete_member(self, request, pk=None, user_id=None):
        project = self.get_object()
        serializer = ProjectMemberSerializer(data={"user": user_id})
        serializer.is_valid(raise_exception=True)

        updated = ProjectService.delete_member(
            project, serializer.validated_data["user"]
        )

        return Response(ProjectSerializer(updated).data, status=status.HTTP_200_OK)
