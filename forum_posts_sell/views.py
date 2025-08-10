from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import Create_Form
from .models import Post
# Create your views here.

def print_post(request):
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(Author=request.user)
    else:
        return redirect("/register/")
    return render(request,"forum_posts/print.html",{"user_posts":user_posts})

def create_post(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            form = Create_Form(request.POST)
            if form.is_valid():
                Title = form.cleaned_data["title"]  
                Tags = form.cleaned_data["tags"]
                if len(Tags) <= 1:
                    return HttpResponse('Bad tag')
                Message = form.cleaned_data["text"]
                print(Title,Tags,Message)
                post = Post.objects.create(Title=Title,Text=Message,Author=request.user)
                tags_list = [tag.strip() for tag in Tags.split(',')]
                post.tags.set(tags_list)
                return HttpResponse(f'{Title,Tags,Message,request.user}')
        else:
            form = Create_Form()
    else:
        return redirect("/register/")
    return render(request, "forum_posts/create.html", {"form": form})

def edit_post(request, id):
    if request.user.is_authenticated:
        print('cwel')
    else:
        return redirect("/register/")
    return HttpResponse(f'edit działa {id}')

def delete_post(request, id):
    if request.user.is_authenticated:
        print('cwel')
    else:
        return redirect("/register/")
    return HttpResponse(f'delete działa {id}')
