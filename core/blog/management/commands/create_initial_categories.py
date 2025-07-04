from django.core.management.base import BaseCommand
from blog.models import Category


class Command(BaseCommand):
    help = "Create initial categories for the blog"

    def handle(self, *args, **kwargs):
        categories = [
            {"name": "Technology", "color": "#85CAE9"},
            {"name": "Health", "color": "#92CF94"},
            {"name": "Lifestyle", "color": "#DCD271"},
            {"name": "Travel", "color": "#9C8645"},
            {"name": "Food", "color": "#E0896E"},
            {"name": "Education", "color": "#A387D6"},
            {"name": "Finance", "color": "#E43CC8"},
            {"name": "Entertainment", "color": "#D45050"},
        ]

        for item in categories:
            category, created = Category.objects.get_or_create(
                name=item["name"],
                defaults={"color": item["color"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {category.name}"))

        self.stdout.write(self.style.SUCCESS("Successfully created initial categories"))
