from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('my-recipes/', views.MyRecipesListView.as_view(), name='my-recipes'),
    path('create/', views.RecipeCreateView.as_view(), name='recipe-create'),
    path('<slug:slug>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('<slug:slug>/update/', views.RecipeUpdateView.as_view(), name='recipe-update'),
    path('<slug:slug>/delete/', views.RecipeUpdateView.as_view(), name='recipe-delete'),
]