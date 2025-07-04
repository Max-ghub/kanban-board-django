from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, phone, username, password, **extra_fields):
        if not phone:
            raise ValueError("Номер телефона не был указан")
        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, username, password, **extra_fields):
        return self._create_user(phone, username, password, **extra_fields)

    def create_superuser(self, phone, username, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(phone, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=12, unique=True)
    username = models.CharField(max_length=16, unique=True, blank=False)
    name = models.CharField(max_length=24, blank=True)
    surname = models.CharField(max_length=28, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    def get_short_name(self):
        return self.name or self.username

    def __str__(self):
        return f"{self.get_short_name()} ({self.phone})"

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
