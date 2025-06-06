from django.urls import path
from . import views
from .views import HomeView, FileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('media/<uuid:file_id>/', views.secure_media_view, name='secure_media'),
    path('folder/<uuid:pk>/', FileView.as_view(), name='dtfiles'),
    path('delete-folder/<uuid:pk>/', views.delete_folder, name='delete_folder'),
    path('delete-file/<uuid:pk>/', views.delete_file, name='delete_file'),
    path('copy-file/<uuid:pk>/', views.copy_file, name='copy_file'),
    path('move-file/<uuid:pk>/', views.move_file, name='move_file'),
    path('create-folder/', views.create_folder_view, name='create_folder'),
    path('add-file/', views.add_file_view, name='add_file'),
    path('search/', views.search_view, name='search'),
]
