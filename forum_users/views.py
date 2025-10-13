from django.shortcuts import render
from django.shortcuts import redirect
from .models import CustomUser
# Create your views here.
    
def view_account(request):
    if not request.user.is_authenticated:
        return redirect("/register/")
    user_data = CustomUser.objects.filter(id=request.user.id).get()
    return render(request, 'forum_users/account.html', {'user_data': user_data})