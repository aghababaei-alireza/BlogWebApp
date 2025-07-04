from django.core.management.base import BaseCommand
from faker import Faker
from account.models import User


class Command(BaseCommand):
    help = "Create test users for the application"

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = []

        for _ in range(3):  # Create 10 test users
            user = User(
                username=f"test_{fake.user_name()}",
                email=fake.email(),
            )
            user.set_password(fake.password())
            users.append(user)

        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS("Successfully created test users"))
