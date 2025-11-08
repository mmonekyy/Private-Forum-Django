from django.urls import path 
from .views import points, ranks, leaderboard , buy_Super_Vip , buy_Vip , execute_payment, payment_checkout ,payment_failed
urlpatterns = [
path('', points, name='Money'),
path('ranks/', ranks, name='ranks'),
path('leaderboard/', leaderboard, name='leaderboard'),
path('checkout/', payment_checkout, name='checkout_payment'),
path('buy_Super_Vip/', buy_Super_Vip, name='buy_Super_Vip_payment'),
path('buy_Vip/', buy_Vip, name='buy_Vip_payment'),
path('execute_payment/', execute_payment, name='execute_payment'),
path('payment_failed', payment_failed, name='payment_failed')
]