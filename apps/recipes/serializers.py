# apps/recipes/serializers.py
from rest_framework import serializers
from .models import Recipe
from apps.categories.serializers import CategorySerializer
from apps.users.serializers import UserProfileSerializer

class RecipeSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    average_rating = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'slug', 'description', 'ingredients', 'instructions',
            'image', 'image_url', 'author', 'categories', 'category_ids', 
            'is_draft', 'is_public', 'created_at', 'updated_at', 'average_rating'
        )
        read_only_fields = ('id', 'slug', 'author', 'created_at', 'updated_at', 'average_rating', 'image_url')
    
    def get_average_rating(self, obj) -> float | None:
        return obj.average_rating()

    def get_image_url(self, obj) -> str | None:
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        recipe = Recipe.objects.create(**validated_data)
        
        if category_ids:
            recipe.categories.set(category_ids)
        
        return recipe

class RecipeListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'slug', 'description', 'image', 'author_name',
            'created_at', 'average_rating'
        )
    
    def get_average_rating(self, obj) -> float | None:
        return obj.average_rating()