from django.db import models

from users.models import User

from .base_model import BaseManagementModel


class Project(BaseManagementModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_projects"
    )
    members = models.ManyToManyField(User, related_name="member_projects")
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=2048, blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "management_projects"
