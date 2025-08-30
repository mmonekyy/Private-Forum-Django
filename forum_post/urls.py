from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from .views import create

def hello(request):
    return HttpResponse("Hello, world!")

urlpatterns = [
    path('',hello),
    path('Create/<int:category_id>/',create, name='create_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
