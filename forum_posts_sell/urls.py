from django.urls import path , include
from .views import create_post , edit_post , print_post

app_name = 'posts_sell'

urlpatterns = [
    path('',print_post),
    path('create/',(create_post), name='create'),
    path('edit/<int:id>/',edit_post),
    path('delete/<int:id>/',print_post),
]
