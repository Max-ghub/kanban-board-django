from django.contrib import admin

from .models import NotificationPreferences


@admin.register(NotificationPreferences)
class NotificationPreferencesAdmin(admin.ModelAdmin):
    list_display = ("user", "email_enabled", "sms_enabled")
    search_fields = ("user__username", "user__phone")
