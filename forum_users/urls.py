from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse

def dummy_view(request):
    return HttpResponse("This is a placeholder view.")

urlpatterns = [
    path('',dummy_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
