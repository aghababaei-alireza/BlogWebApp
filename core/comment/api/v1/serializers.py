from rest_framework import serializers
from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "published_at", "edited_at"]
        read_only_fields = ["author", "post", "created_at", "updated_at"]
        extra_kwargs = {
            "post": {"required": True},
            "author": {"required": True},
            "content": {"required": True},
        }
