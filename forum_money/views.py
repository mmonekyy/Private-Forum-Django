from django.shortcuts import render
from forum_users.models import CustomUser
from .models import Button
import datetime
from django.utils import timezone
from django.http import HttpResponse
import random
# Create your views here.
def points(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated')
    
    def money_User(radomint_1,randomint_2,button_object):
        obj = button_object.get()
        obj.next_roll = datetime.datetime.now() + datetime.timedelta(hours=1)
        obj.save()
        money = random.randint(radomint_1, randomint_2)
        user = CustomUser.objects.get(username=request.user)
        user.user_money += money
        user.save()

    def button_verifi(button_object):
        test =  (button_object.get().next_roll)
        print(datetime.datetime.now())
        print(test)
        if test == None or test <= timezone.now():
            return(True)
        else:
            return(False)
    but = Button.objects.filter(user=request.user)
    if but.exists():
        pass
    else:
        Button.objects.create(user=request.user)
        print('Create')
    value = button_verifi(but)
    print(value)
    points_randomizer  = random.randint(0,10)
    if request.method == "POST" and value == True: 
        if points_randomizer  <= 5:
            money_User(0, 200,but)
        elif 5 < points_randomizer  <= 9:
            money_User(50, 400,but)
        else :
            money_User(400, 1000,but)
    else:
        if request.method == "POST" and value == False:
            return HttpResponse('You can press the button every hour')
    return render(request, 'forum_money/money.html')

# add paypal payments 
def ranks(request):

    return render(request, 'forum_money/ranks.html')

def leaderboard(request):
    bestusers = CustomUser.objects.all().order_by('-user_money')[:10]
    return render(request, 'forum_money/leaderboard.html',{"BestUsers":bestusers})
