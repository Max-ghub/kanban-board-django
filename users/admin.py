from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("phone", "username", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser", "date_joined")
    search_fields = ("phone", "username", "is_active", "is_staff", "is_superuser")
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        ("Основные данные", {"fields": ("phone", "username")}),
        ("Персональная информация", {"fields": ("name", "surname")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            "Основные данные",
            {"fields": ("phone", "username", "password1", "password2")},
        ),
        ("Персональная информация", {"fields": ("name", "surname")}),
        ("Права доступа", {"fields": ("is_active",)}),
    )
