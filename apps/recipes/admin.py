from django.contrib import admin
from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "is_draft",
        "is_public",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_draft", "is_public", "categories", "created_at")
    search_fields = (
        "title",
        "author__email",
        "author__first_name",
        "author__last_name",
    )
    list_editable = ("is_draft", "is_public")
    list_display_links = ("title",)
    filter_horizontal = ("categories",)
    readonly_fields = ("slug", "created_at", "updated_at")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "author", "description", "image")},
        ),
        ("Content", {"fields": ("ingredients", "instructions")}),
        ("Categorization", {"fields": ("categories",)}),
        ("Status", {"fields": ("is_draft", "is_public")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author")


admin.site.register(Recipe, RecipeAdmin)
