from django.urls import path
from . import views

urlpatterns = [
    path('upload-file/', views.FileUploadView.as_view(), name='file-upload'),
]