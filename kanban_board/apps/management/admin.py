from django.contrib import admin

from .models import Board, Column, Project, RelationTask, Task


class CustomProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_archived", "created_at")
    search_fields = ("owner", "title")
    ordering = ("owner", "title")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("updated_at", "created_at")


class CustomBoardAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("project", "created_at", "updated_at")
    ordering = ("project", "title")
    readonly_fields = ("created_at", "updated_at")


class CustomColumnAdmin(admin.ModelAdmin):
    list_display = ("title", "board", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("board", "created_at", "updated_at")
    ordering = ("board", "title")
    readonly_fields = ("created_at", "updated_at")


class CustomTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "column", "assignee", "status", "priority", "created_at")
    search_fields = ("title", "assignee__username")
    list_filter = ("status", "priority", "created_at", "updated_at")
    ordering = ("column", "title")
    readonly_fields = ("created_at", "updated_at")


class RelationTaskAdmin(admin.ModelAdmin):
    list_display = ("from_task", "relation_type", "to_task")
    list_filter = ("relation_type",)
    search_fields = ("from_task__title", "to_task__title")


admin.site.register(Project, CustomProjectAdmin)
admin.site.register(Board, CustomBoardAdmin)
admin.site.register(Column, CustomColumnAdmin)
admin.site.register(Task, CustomTaskAdmin)
admin.site.register(RelationTask, RelationTaskAdmin)
