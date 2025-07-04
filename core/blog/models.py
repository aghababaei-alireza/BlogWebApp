from django.db import models
from account.models import User
import random
from django.utils.html import mark_safe


def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name", unique=True)
    color = models.CharField(max_length=7, default=random_color)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def color_badge(self):
        return mark_safe(
            f'<span style="display:inline-block;width:15px;height:15px;background:{self.color};border-radius:50%;"></span>'
        )

    color_badge.short_description = "Color"


class Post(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    content = models.TextField()
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
