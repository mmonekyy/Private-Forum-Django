from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from .views import events, event
urlpatterns = [
    path('',events , name='events'),
    path('Event/<int:event_id>/',event , name='event'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
