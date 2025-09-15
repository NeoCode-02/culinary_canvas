from django.contrib import admin
from .models import Comment, Rating


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", "created_at", "is_edited", "updated_at")
    list_filter = ("is_edited", "created_at")
    search_fields = ("user__email", "recipe__title", "content")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Content", {"fields": ("user", "recipe", "content")}),
        ("Status", {"fields": ("is_edited",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "recipe")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", "score", "created_at", "updated_at")
    list_filter = ("score", "created_at")
    search_fields = ("user__email", "recipe__title")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Rating Details", {"fields": ("user", "recipe", "score")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "recipe")
