# python manage.py generate_all --user_count 15 --projects_count 8 --seed 123

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run both user generation and project/demo generation commands"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user_count",
            type=int,
            default=10,
            help="Number of users to create in first step",
        )
        parser.add_argument(
            "--projects_count",
            type=int,
            default=5,
            help="Number of projects to create in second step",
        )
        parser.add_argument(
            "--seed",
            type=int,
            help="Seed for reproducibility, forwarded to project generator",
        )

    def handle(self, *args, **options):
        user_count = options.get("user_count", 10)
        projects_count = options.get("projects_count", 5)
        seed = options.get("seed")
        self.stdout.write(
            self.style.NOTICE(f"Generating {user_count} users with notifications...")
        )
        call_command("generate_users", "--count", str(user_count))
        self.stdout.write(
            self.style.NOTICE(f"Generating {projects_count} projects demo...")
        )
        cmd_args = ["--projects-count", str(projects_count)]
        if seed is not None:
            cmd_args += ["--seed", str(seed)]
        call_command("generate_projects", *cmd_args)
        self.stdout.write(self.style.SUCCESS("Demo data generation completed."))
