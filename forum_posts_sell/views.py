from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import Create_Form
from .models import sell_post
from .support_function_views import check_user_type
# Create your views here.

def print_post(request):
    if request.user.is_authenticated:
        user_posts = sell_post.objects.filter(Author=request.user)
    else:
        return redirect("/register/")
    return render(request,"forum_posts/print.html",{"user_posts":user_posts})

def create_post(request):
    if request.user.is_authenticated:
        user_check_result = check_user_type(request)
        if user_check_result:  
            return user_check_result
        if request.method =="POST":
            form = Create_Form(request.POST)    
            if form.is_valid():
                Title = form.cleaned_data["title"]  
                Tags = form.cleaned_data["tags"]
                Price = form.cleaned_data["price"]
                if Price < 0:
                    return HttpResponse('Price cannot be negative')
                if len(Title) < 5:
                    return HttpResponse('Title is too short')
                if len(Title) > 100:
                    return HttpResponse('Title is too long')
                if len(Tags) > 100:
                    return HttpResponse('Tags are too long')
                if len(Tags) < 3:
                    return HttpResponse('Tags are too short')
                Message = form.cleaned_data["text"]
                print(Title,Tags,Message,Price)
                post = sell_post.objects.create(Title=Title,Text=Message,Author=request.user, Price=Price)
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
        Post_user = sell_post.objects.filter(id=id, Author=request.user)
        if Post_user.exists():
            Post_user.get()
            return HttpResponse(f'edit działa {Post_user}')
        else:
            return HttpResponse('Post not found or you are not the author.')
    else:
        return redirect("/register/")

def delete_post(request, id):
    if request.user.is_authenticated:
        print('cwel')
    else:
        return redirect("/register/")
    return HttpResponse(f'delete działa {id}')
