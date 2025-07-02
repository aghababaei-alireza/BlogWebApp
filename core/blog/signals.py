from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Post


@receiver(pre_save, sender=Post)
def delete_old_image(sender: Post, instance: Post, **kwargs):
    if not instance.pk:
        return  # Skip new instances

    try:
        old_image = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return

    # If new image is different from old one
    if old_image and old_image != instance.image:
        old_image.delete(save=False)


@receiver(post_delete, sender=Post)
def auto_delete_image_on_delete(sender: Post, instance: Post, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
