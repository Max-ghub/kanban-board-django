from django.contrib import admin

from .models import PhoneCode


@admin.register(PhoneCode)
class PhoneCodeAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "attempts", "created_at")
    list_filter = ("created_at",)
    search_fields = ("phone", "code")
    readonly_fields = ("created_at",)
