from django.shortcuts import render, redirect, get_object_or_404
from forum_users.models import CustomUser
from .models import Button, Vips
import datetime
from django.utils import timezone
from django.http import HttpResponseBadRequest
import random
import paypalrestsdk
from django.urls import reverse

def points(request):
    if not request.user.is_authenticated:
        return redirect("/register/")

    def money_User(randomint_1, randomint_2, button_object):
        obj = button_object.get()
        obj.next_roll = timezone.now() + datetime.timedelta(hours=1)
        obj.save()
        money = random.randint(randomint_1, randomint_2)
        user = CustomUser.objects.get(username=request.user)
        user.user_money += money
        user.save()
        return False

    def button_verifi(button_object):
        test = button_object.get().next_roll
        return test is None or test <= timezone.now()

    but = Button.objects.filter(user=request.user)
    if not but.exists():
        Button.objects.create(user=request.user)
        but = Button.objects.filter(user=request.user)

    value = button_verifi(but)

    if request.method == "POST" and value:
        points_randomizer = random.randint(0, 10)
        if points_randomizer <= 5:
            money_User(0, 200, but)
        elif 5 < points_randomizer <= 9:
            money_User(50, 400, but)
        else:
            money_User(400, 1000, but)
        value = button_verifi(but)

    return render(request, 'forum_money/money.html', {
        "money_win": value,
        "next_roll": but.get().next_roll,
        "current_money": CustomUser.objects.get(username=request.user).user_money
    })

def ranks(request):
    if not request.user.is_authenticated:
        return redirect("/register/")
    return render(request, 'forum_money/ranks.html')

def create_paypal_payment(request, amount, description):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": description,
                    "sku": "item",
                    "price": f"{amount:.2f}",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {"total": f"{amount:.2f}", "currency": "USD"},
            "description": description
        }]
    })
    return payment


def buy_Vip(request):
    if not request.user.is_authenticated:
        return redirect("/register/")

    payment = create_paypal_payment(request, 10.00, "VIP Membership")

    if payment.create():
        Vips.objects.create(
            user=request.user,
            payment_id=payment.id,
            amount=10,
            status='created'
        )
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        print(payment.error)
        return render(request, 'forum_money/error.html', {"error": payment.error})


def buy_Super_Vip(request):
    if not request.user.is_authenticated:
        return redirect("/register/")

    payment = create_paypal_payment(request, 20.00, "Super VIP Membership")

    if payment.create():
        Vips.objects.create(
            user=request.user,
            payment_id=payment.id,
            amount=20,
            status='created'
        )
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        print(payment.error)
        return render(request, 'forum_money/error.html', {"error": payment.error})

def execute_payment(request):
    if not request.user.is_authenticated:
        return redirect("/register/")

    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    vip_payment = get_object_or_404(Vips, payment_id=payment_id, user=request.user)
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        vip_payment.status = 'approved'
        vip_payment.payer_id = payer_id
        vip_payment.save()
        user = request.user
        if vip_payment.amount == 10:
            user.user_type = CustomUser.UserType.VIP
        elif vip_payment.amount == 20:
            user.user_type = CustomUser.UserType.SVIP
        user.save()
        return render(request, 'forum_money/success.html', {"vip": vip_payment})
    else:
        vip_payment.status = 'failed'
        vip_payment.save()
        return render(request, 'forum_money/error.html', {"error": payment.error})

def payment_checkout(request):
    if not request.user.is_authenticated:
        return redirect("/register/")
    return render(request, 'forum_money/checkout.html')

def payment_failed(request):
    if not request.user.is_authenticated:
        return redirect("/register/")
    return render(request, 'forum_money/payment_failed.html')

def leaderboard(request):
    if not request.user.is_authenticated:
        return redirect("/register/")
    bestusers = CustomUser.objects.all().order_by('-user_money')[:10]
    return render(request, 'forum_money/leaderboard.html', {"BestUsers": bestusers})
