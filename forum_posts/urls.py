from django.urls import path , include
from .views import create_post , edit_post , print_post
urlpatterns = [
    path('',print_post),
    path('create/',create_post),
    path('edit/<int:id>/',edit_post),
    path('delete/<int:id>/',print_post),
]
