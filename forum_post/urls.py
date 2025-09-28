from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from .views import create , view_own_post , edit , delete ,view_all_posts, view_post , add_comment

urlpatterns = [
    path('',view_all_posts),
    path('Post/<int:post_id>/',view_post, name='view_post'),
    path('Post/<int:post_id>/comment/',add_comment, name='comment'),
    path('Create/',create, name='create_post'),
    path('ViewOwnPosts/',view_own_post, name='view_own_posts'),
    path('ViewOwnPosts/Edit/<int:post_id>/',edit, name='edit_post'),
    path('Delete/<int:post_id>/',delete, name='delete_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
