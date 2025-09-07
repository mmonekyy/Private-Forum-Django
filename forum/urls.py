from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from .views import forum_main
urlpatterns = [
    path('',forum_main),
    path('Marketplace/',include("forum_posts_sell.urls")),
    path('AdminPanel/',include("admin_panel.urls")),
    path('Account/',include("forum_users.urls")),
    path('Events/',include("forum_events.urls")),
    path('Posts/',include("forum_post.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
