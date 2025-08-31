from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from .views import create , view_own_post , edit , delete 

def hello(request):
    return HttpResponse("Hello, world!")

urlpatterns = [
    path('',hello),
    path('Create/<int:category_id>/',create, name='create_post'),
    path('ViewOwnPosts/',view_own_post, name='view_own_posts'),
    path('Edit/<int:post_id>/',edit, name='edit_post'),
    path('Delete/<int:post_id>/',delete, name='delete_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
