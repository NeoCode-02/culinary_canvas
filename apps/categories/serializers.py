from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class CategoryListSerializer(serializers.ModelSerializer):
    recipe_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'recipe_count', 'created_at')