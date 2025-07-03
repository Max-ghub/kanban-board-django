from django.contrib import admin

from .models import Board, Column, Project, RelationTask, Task


class BoardInline(admin.TabularInline):
    model = Board
    extra = 0
    fields = ("title",)
    readonly_fields = ()
    show_change_link = True


class ColumnInline(admin.TabularInline):
    model = Column
    extra = 0
    fields = ("title", "order")
    ordering = ("order",)
    show_change_link = True


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("title", "assignee", "status", "priority")
    show_change_link = True


class OutgoingRelationInline(admin.TabularInline):
    model = RelationTask
    fk_name = "from_task"
    extra = 0
    fields = ("to_task", "relation_type")
    verbose_name = "Исходящая связь"
    verbose_name_plural = "Исходящие связи"


class IncomingRelationInline(admin.TabularInline):
    model = RelationTask
    fk_name = "to_task"
    extra = 0
    fields = ("from_task", "relation_type")
    verbose_name = "Входящая связь"
    verbose_name_plural = "Входящие связи"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("owner", "title", "is_archived", "task_completed_percent")
    list_filter = ("owner", "is_archived")
    fields = ("title", "description", "owner", "members", "is_archived", "task_completed_percent")
    search_fields = ("title", "description", "owner__username", "owner__phone")
    filter_horizontal = ("members",)
    readonly_fields = ("task_completed_percent",)
    ordering = ("owner",)
    inlines = [BoardInline]

    def task_completed_percent(self, obj):
        total = Task.objects.filter(column__board__project=obj).count()
        if total == 0:
            return "—"
        done = Task.objects.filter(column__board__project=obj, status=Task.TaskStatus.DONE).count()
        return f"{(done / total) * 100:.0f}%"
    task_completed_percent.short_description = "Выполнено задач"


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "project")
    list_filter = ("project",)
    search_fields = ("title", "project__title")
    ordering = ("project",)
    inlines = [ColumnInline]

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ("title", "board", "order")
    list_filter = ("board",)
    search_fields = ("title", "board__title")
    ordering = ("board__title", "order")
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "column", "assignee", "status", "priority")
    list_filter = ("assignee", "priority", "status")
    search_fields = ("title", "description", "assignee__username", "assignee__phone")
    inlines = [OutgoingRelationInline, IncomingRelationInline]
    ordering = ("column",)
    fields = (
        "title",
        "description",
        "column",
        "parent",
        "assignee",
        "priority",
        "status",
        "estimated_time",
        "actual_time",
    )


@admin.register(RelationTask)
class RelationTaskAdmin(admin.ModelAdmin):
    list_display = ("from_task", "to_task", "relation_type")
    list_filter = ("relation_type",)
    search_fields = (
        "from_task__title",
        "to_task__title",
        "from_task__assignee__username",
        "to_task__assignee__username",
    )
