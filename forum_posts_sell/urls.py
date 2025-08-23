from django.urls import path , include
from .views import create_post , edit_post , print_post , delete_post , marketplace , marketplace_one_product

app_name = 'posts_sell'

urlpatterns = [
    path('MyProducts/',print_post, name='print_post'),
    path('',marketplace, name='comunity_posts'),
    path('product/<int:id>/',marketplace_one_product, name='one_product'),
    path('create/',create_post, name='create_post'),
    path('edit/<int:id>/',edit_post,name='edit_post'),
    path('delete/<int:id>/',delete_post, name='delete_post'),
]
