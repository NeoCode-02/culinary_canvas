from django.db import models
from django.conf import settings


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.email} on {self.recipe.title}"


class Rating(models.Model):
    SCORE_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings"
    )
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.CASCADE, related_name="ratings"
    )
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "recipe"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.score} stars by {self.user.email} for {self.recipe.title}"
