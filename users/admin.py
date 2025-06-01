from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "name",
        "surname",
        "is_active",
        "is_staff",
        "date_joined",
    )
    search_fields = ("phone", "username", "name", "surname")
    ordering = ("username",)
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")

    fieldsets = (
        (None, {"fields": ("phone", "username", "password")}),
        ("Personal info", {"fields": ("name", "surname")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "username",
                    "name",
                    "surname",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    readonly_fields = ("date_joined", "last_login")


admin.site.register(User, CustomUserAdmin)
