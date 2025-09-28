from django.shortcuts import render
from forum_users.models import CustomUser
from .models import Button
import datetime
from django.http import HttpResponse
import random
# Create your views here.
def points(request):
    def money_User(radomint_1,randomint_2):
        money = random.randint(radomint_1, randomint_2)
        user = CustomUser.objects.get(username=request.user)
        user.user_money += money
        user.save()
    points_randomizer  = random.randint(0,10)
    try:
        button_timer = Button.objects.get(user=request.user)
    except :
        pass
    if request.method == "POST":
        if points_randomizer  <= 5:
            money_User(0, 200)
        elif 5 < points_randomizer  <= 9:
            money_User(50, 400)
        else :
            money_User(400, 1000)

    return render(request, 'forum_money/money.html')

# add paypal payments 
def ranks(request):

    return render(request, 'forum_money/ranks.html')

def leaderboard(request):
    bestusers = CustomUser.objects.all().order_by('-user_money')[:10]
    return render(request, 'forum_money/leaderboard.html',{"BestUsers":bestusers})
