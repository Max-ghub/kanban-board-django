from django.contrib import admin

from .models import Notification, NotificationSettings


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "show_unread_only")
    search_fields = ("user__username", "user__phone")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "type", "is_read", "created_at")
    list_filter = ("type", "is_read", "created_at")
    search_fields = ("title", "message", "user__username", "user__phone")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    fields = (
        "user",
        "type",
        "title",
        "message",
        "url",
        "is_read",
        "created_at",
        "updated_at",
    )
