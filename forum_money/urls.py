from django.urls import path 
from .views import points, ranks, leaderboard
urlpatterns = [
path('points/', points, name='points'),
path('ranks/', ranks, name='ranks'),
path('leaderboard/', leaderboard, name='leaderboard'),
]