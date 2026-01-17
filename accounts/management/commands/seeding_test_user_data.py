from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import Project, Users, ProjectUserMapping


class Command(BaseCommand):
    help = "Seed database with sample projects, users, and mappings"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("🚀 Seeding database...")

        # --------------------
        # Projects
        # --------------------
        project_email, _ = Project.objects.get_or_create(
            name="Acme Analytics",
            defaults={
                "description": "Analytics dashboard for enterprises",
                "auth_type": "email",
            },
        )

        project_username, _ = Project.objects.get_or_create(
            name="Dev Playground",
            defaults={
                "description": "Internal developer platform",
                "auth_type": "username",
            },
        )

        self.stdout.write("✅ Projects created")

        # --------------------
        # Users
        # --------------------
        users_data = [
            {"email": "alice@gmail.com", "user_data": {"country": "India"}},
            {"email": "bob@gmail.com", "user_data": {"country": "USA"}},
            {"username": "charlie_dev", "user_data": {"github": "charlie"}},
            {"username": "david_ops", "user_data": {"role": "ops"}},
            {
                "email": "eve@gmail.com",
                "username": "eve_admin",
                "user_data": {"role": "admin"},
            },
        ]

        users = []
        for data in users_data:
            user, _ = Users.objects.get_or_create(**data)
            users.append(user)

        self.stdout.write("✅ Users created")

        # --------------------
        # Project Mappings
        # --------------------
        mappings = [
            (project_email, "alice@gmail.com"),
            (project_email, "bob@gmail.com"),
            (project_email, "eve@gmail.com"),
            (project_username, "charlie_dev"),
            (project_username, "david_ops"),
            (project_username, "eve_admin"),
        ]

        for project, identifier in mappings:
            if project.auth_type == "email":
                user = Users.objects.get(email=identifier)
            else:
                user = Users.objects.get(username=identifier)

            ProjectUserMapping.objects.get_or_create(
                project=project,
                user=user,
            )

        self.stdout.write("✅ Project-user mappings created")
        self.stdout.write(self.style.SUCCESS("🎉 Database seeded successfully"))
