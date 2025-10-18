from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
def test_view(request):
    return HttpResponse("Admin Panel Works!")
urlpatterns = [
    path('',test_view , name='forum_main'),
    path('sellpost/', test_view, name='forum_sellpost'),
] 
