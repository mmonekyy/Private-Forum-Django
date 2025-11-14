from django.shortcuts import render
from django.shortcuts import redirect
from .models import CustomUser
from forum_register.models import Keys , User_gen_kay
from django.utils.crypto import get_random_string
    
def view_account(request):
    if not request.user.is_authenticated:
        return redirect("/register/")
    user_data = CustomUser.objects.filter(id=request.user.id).get()
    return render(request, 'forum_users/account.html', {'user_data': user_data})

def get_key(request):
    if not request.user.is_authenticated:
        return redirect("/register/")
    user = request.user
    user_keys = User_gen_kay.objects.filter(User=user)
    valid = 0
    message = None
    
    if user_keys.exists():
        valid = 1
        message = "You can have only one key"
        user_key = user_keys.first()
    else:
        user_key = None

    if request.method == "POST" and valid == 0:
        key = get_random_string(256)
        generated_key = Keys.objects.create(key=key)
        user_key = User_gen_kay.objects.create(User=user, key=generated_key)
        message = "Key successfully generated!"

    return render(request, 'forum_users/key.html', {
        "message": message,
        "User_key": user_key
    })