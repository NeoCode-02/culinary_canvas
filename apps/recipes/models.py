from django.db import models
from django.conf import settings


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=500)
    ingredients = models.TextField(
        help_text="List ingredients with measurements, one per line"
    )
    instructions = models.TextField(
        help_text="Step-by-step instructions including preparation and cooking time if needed"
    )
    image = models.ImageField(upload_to="recipe_images/")
    categories = models.ManyToManyField("categories.Category", related_name="recipes")
    is_draft = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.score for rating in ratings) / len(ratings)
        return 0
