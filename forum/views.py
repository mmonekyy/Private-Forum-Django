from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def forum_main(request):
    if request.user.is_authenticated:
        if request.user.is_regular_user():
            return render(request, 'forum/forum.html')
        else:
            return HttpResponse("other user")
    else:
        return redirect("/register/")
    