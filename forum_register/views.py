from django.shortcuts import render , redirect
from .forms import RegisterForm , LoginForm
from forum_users.models import CustomUser
from .models import Keys
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_GET
import logging
logger = logging.getLogger(__name__)
# Create your views here.

def register(request):
    if request.method == "POST":
        if 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                key = register_form.cleaned_data["key"]
                username = register_form.cleaned_data["username"]
                password = register_form.cleaned_data["password"]
                password2 = register_form.cleaned_data["password2"]
                if not CustomUser.objects.filter(username=username).exists() and Keys.objects.filter(key=key).exists() and password == password2:
                    CustomUser.objects.create_user(username=username,password=password)
                    Keys.objects.filter(key=key).delete()
                    user = authenticate(request,username=username,password=password)
                    if user:
                        login(request, user)
                elif CustomUser.objects.filter(username=username).exists():
                    logger.info("username exist")
                elif not Keys.objects.filter(key=key).exists():
                    logger.info("bad key")
                elif password != password2:
                    logger.info("passwords do not match")

        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(request,username=username,password=password)
                if user:
                    login(request, user)
                    return redirect("/")
                else:
                    print("bad data")
    return render(request,"register/index.html",{'Register_form':RegisterForm,'Login_form':LoginForm})

