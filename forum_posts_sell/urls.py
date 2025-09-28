from django.urls import path 
from .views import create_post , edit_post , print_post , delete_post , marketplace , marketplace_one_product , buy_product ,user_items , item_detail

app_name = 'posts_sell'

urlpatterns = [
    path('',marketplace, name='marketplace'),
    path('MyProducts/',print_post, name='print_post'),
    path('create/',create_post, name='create_post'),
    path('edit/<int:id>/',edit_post,name='edit_post'),
    path('delete/<int:id>/',delete_post, name='delete_post'),
    path('product/<int:id>/',marketplace_one_product, name='one_product'),
    path('buy/<int:id>/',buy_product, name='buy_product'),
    path('MyItems/',user_items, name='user_items'),
    path('MyItems/item_detail/<int:id>/',item_detail, name='item_detail'),
]
