from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from .views import modpanel , check_post_sell , get_one_post_sell , approve_post_sell , delete_post_sell , check_post , get_one_post  , delete_post , delete_comment

namespace = 'admin_panel'

urlpatterns = [
    path('',modpanel , name='forum_main'),
    path('sellpost/', check_post_sell, name='forum_sellpost'),
    path('sellpost/<int:post_id>/', get_one_post_sell, name='one_post_sell'),
    path('sellpost/approve/<int:post_id>/', approve_post_sell, name='approve_post_sell'),
    path('sellpost/delete/<int:post_id>/', delete_post_sell, name='delete_post_sell'),
    path('post/', check_post, name='forum_post'),
    path('post/<int:post_id>/', get_one_post, name='one_post'),
    path('post/delete/<int:post_id>/', delete_post, name='delete'),
    path('post/comment/delete/<int:command_id>/', delete_comment, name='delete_comment'),
] 
