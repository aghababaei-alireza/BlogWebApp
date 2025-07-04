from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Category, Post
from account.models import User


class Command(BaseCommand):
    help = "Create fake posts for the blog"

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = Category.objects.all()

        if not categories:
            self.stdout.write(self.style.ERROR("No categories found. Please create categories first."))
            return

        users = User.objects.filter(username__startswith="test_")
        if not users:
            self.stdout.write(self.style.ERROR("No test users found. Please create test users first."))
            return

        for _ in range(10):  # Create 10 fake posts
            category = fake.random.choice(categories)
            user = fake.random.choice(users)
            post = Post.objects.create(
                title=fake.sentence(),
                content=fake.text(),
                category=category,
                author=user,
            )
            self.stdout.write(self.style.SUCCESS(f"Created post: {post.title} in category: {category.name}"))

        self.stdout.write(self.style.SUCCESS("Successfully created fake posts"))
