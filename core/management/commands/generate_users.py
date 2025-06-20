# python manage.py generate_users --count 15

import random

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from notification.models import Notification, NotificationSettings
from notification_preferences.models import NotificationPreferences
from users.models import User


class Command(BaseCommand):
    help = "Generate random users with notification settings, preferences and notifications"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of users to create"
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options.get("count", 10)
        created = 0
        attempts = 0
        max_attempts = count * 3
        while created < count and attempts < max_attempts:
            attempts += 1
            phone = "".join(
                fake.random_choices(elements=[str(i) for i in range(10)], length=11)
            )
            username = fake.user_name()[:16]
            name = fake.first_name()
            surname = fake.last_name()
            password = "password123"
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        phone=phone,
                        username=username,
                        password=password,
                        name=name,
                        surname=surname,
                        is_active=True,
                    )
                    NotificationSettings.objects.get_or_create(user=user)
                    NotificationPreferences.objects.get_or_create(user=user)
                    notif_count = random.randint(1, 20)
                    types = [
                        choice[0] for choice in Notification.NotificationType.choices
                    ]
                    for _ in range(notif_count):
                        ntype = random.choice(types)
                        title = ntype.replace("_", " ").title()
                        message = fake.text(max_nb_chars=200)
                        url = fake.url() if random.choice([True, False]) else None
                        is_read = random.choice([True, False])
                        Notification.objects.create(
                            user=user,
                            title=title,
                            message=message,
                            is_read=is_read,
                            type=ntype,
                            url=url,
                        )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user {user} with {notif_count} notifications"
                    )
                )
                created += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating user or related settings: {e}")
                )
                continue
        self.stdout.write(
            self.style.SUCCESS(f"Total users created: {created} (attempts: {attempts})")
        )
