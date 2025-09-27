from rest_framework import serializers

from management.models import Task


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "column",
            "parent",
            "assignee",
            "priority",
            "status",
            "estimated_time",
            "actual_time",
            "updated_at",
            "created_at",
        ]


class TaskMoveSerializer(serializers.Serializer):
    column_id = serializers.IntegerField()


class TaskAssigneeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(allow_null=True)


class TaskSubtaskSerializer(TaskModelSerializer):
    def validate(self, attrs):
        parent_task = self.context.get("parent_task")
        view = self.context.get("view")

        if parent_task is not None and view is not None:
            view._validate_relations(
                column=parent_task.column,
                parent=parent_task,
                assignee=attrs.get("assignee"),
            )

        return super().validate(attrs)

    class Meta(TaskModelSerializer.Meta):
        extra_kwargs = {
            "column": {"read_only": True},
            "parent": {"read_only": True},
        }

    def create(self, validated_data):
        parent_task = self.context.get("parent_task")

        validated_data.update(
            {
                "column": parent_task.column,
                "parent": parent_task,
            }
        )

        return super().create(validated_data)
