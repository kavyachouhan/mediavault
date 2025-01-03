from django.urls import path
from . import views

app_name = 'media_management' 

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_media, name='upload_media'),
]