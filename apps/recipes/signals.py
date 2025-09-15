from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Recipe


@receiver(pre_save, sender=Recipe)
def generate_recipe_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        instance.slug = base_slug

        counter = 1
        while (
            Recipe.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists()
        ):
            instance.slug = f"{base_slug}-{counter}"
            counter += 1


@receiver(post_delete, sender=Recipe)
def delete_recipe_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete()
