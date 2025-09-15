from django.urls import path
from . import views

urlpatterns = [
    # Comments
    path("comments/", views.CommentListView.as_view(), name="comment-list"),
    path("comments/<int:pk>/", views.CommentDetailView.as_view(), name="comment-detail"),
    path("comments/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),

    # Ratings
    path("ratings/", views.RatingListView.as_view(), name="rating-list"),
    path("ratings/<int:pk>/", views.RatingDetailView.as_view(), name="rating-detail"),
    path("ratings/<int:pk>/update/", views.RatingUpdateView.as_view(), name="rating-update"),
    path("ratings/<int:pk>/delete/", views.RatingDeleteView.as_view(), name="rating-delete"),
]
