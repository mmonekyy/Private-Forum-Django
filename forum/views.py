from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def forum_main(request):
    if request.user.is_authenticated:
        return render(request, 'forum/forum.html')
    else:
        return redirect("/register/")
    