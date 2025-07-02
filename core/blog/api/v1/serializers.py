from rest_framework import serializers
from django.urls import reverse
from account.api.v1.serializers import ProfileSerializer
from blog.models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for blog categories.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "color"]
        read_only_fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for blog posts.
    """

    relative_url = serializers.SerializerMethodField(method_name="get_relative_url")
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    def get_relative_url(self, obj):
        return reverse("post:api-v1:posts-detail", kwargs={"pk": obj.pk})

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "category",
            "author",
            "image",
            "content",
            "published",
            "created_at",
            "updated_at",
            "relative_url",
            "absolute_url",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at", "published"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if rep["category"]:
            rep["category"] = CategorySerializer(instance.category).data
        if rep["author"]:
            rep["author"] = ProfileSerializer(instance.author).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
