# apps/recipes/views.py
from rest_framework import generics, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer, RecipeListSerializer

class RecipeListView(generics.ListAPIView):
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'author']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'average_rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Recipe.objects.filter(is_public=True, is_draft=False)

class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.filter(is_public=True, is_draft=False)
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class RecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RecipeUpdateView(generics.UpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'image' in request.FILES and instance.image:
            instance.image.delete(save=False)
        
        return super().update(request, *args, **kwargs)

class RecipeDeleteView(generics.DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

class MyRecipesListView(generics.ListAPIView):
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)
    