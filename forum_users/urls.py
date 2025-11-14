from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from .views import view_account , get_key

urlpatterns = [
    path('',view_account, name='view_account'),
    path('Keys/',get_key ,name='Keys')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
