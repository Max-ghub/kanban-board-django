from django.contrib import admin

from notification.models import Notification, NotificationSettings

admin.site.register(Notification)
admin.site.register(NotificationSettings)
