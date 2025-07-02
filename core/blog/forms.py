from django import forms
from django.core.files.base import ContentFile
import base64
from .models import Category, Post


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["id", "name", "color"]


class PostForm(forms.ModelForm):
    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    delete_image = forms.BooleanField(required=False, label="Clear current image")

    class Meta:
        model = Post
        fields = ["title", "category", "content"]

    def save(self, commit=True):
        instance: Post = super().save(commit=False)

        # Handle deleting the current image
        if self.cleaned_data.get("delete_image") and instance.image:
            instance.image.delete(save=False)
            instance.image = None

        image_data = self.cleaned_data.get("image_data")
        if image_data:
            try:
                format, imgstr = image_data.split(";base64,")
                ext = format.split("/")[-1]
                image_file = ContentFile(base64.b64decode(imgstr), name=f"post_{instance.pk}.{ext}")
                instance.image = image_file
            except Exception:
                pass

        if commit:
            instance.save()

        return instance
