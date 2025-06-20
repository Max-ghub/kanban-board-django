from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("phone", "username", "name", "surname", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("phone", "username", "name", "surname")
    ordering = ("phone",)

    fieldsets = (
        (None, {"fields": ("phone",)}),
        ("Personal info", {"fields": ("username", "name", "surname")}),
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
    readonly_fields = ("last_login", "date_joined")

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
                    "raw_password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)

        class F(Form):
            raw_password = forms.CharField(
                label="Пароль (новый/при создании)",
                required=(obj is None),
                widget=forms.PasswordInput,
                help_text="Введите пароль для нового пользователя или для смены.",
            )

        return F

    def save_model(self, request, obj, form, change):
        raw = form.cleaned_data.get("raw_password")
        if raw:
            obj.set_password(raw)
        else:
            if not change:
                # при создании без введённого raw_password — сгенерировать случайный
                obj.set_password(User.objects.make_random_password())
            # при редактировании без raw_password — оставляем старый пароль
        super().save_model(request, obj, form, change)
