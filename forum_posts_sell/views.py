from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import Create_Form
from .models import sell_post , buyed_item , user_bought_items
from .support_function_views import check_user_type
from forum_users.models import CustomUser
from django.utils import timezone

def print_post(request):
    if request.user.is_authenticated:
        user_posts = sell_post.objects.filter(Author=request.user)
    else:
        return redirect("/register/")
    return render(request,"forum_posts/print.html",{"user_posts":user_posts})

def create_post(request):
    if request.user.is_authenticated:
        user_check_result = check_user_type(request,sell_post, timezone.now(), HttpResponse)
        if user_check_result:  
            return user_check_result
        print(request.user)
        if request.method =="POST":
            print(request.user)
            form = Create_Form(request.POST)    
            if form.is_valid():
                print(request.user)
                Title = form.cleaned_data["title"]  
                Tags = form.cleaned_data["tags"]
                Price = form.cleaned_data["price"]
                Item = form.cleaned_data["item"]
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
                if len(Item) < 10:
                    return HttpResponse('Item is too short')
                Message = form.cleaned_data["text"]
                print(Title,Tags,Message,Price)
                post = sell_post.objects.create(Title=Title,Text=Message,Author=request.user, Price=Price)
                tags_list = [tag.strip() for tag in Tags.split(',')]
                post.tags.set(tags_list)
                buyed_item.objects.create(foring_key_sell_post=post, Text=Item)
                return redirect("posts_sell:print_post")
        else:
            form = Create_Form()
    else:
        return redirect("/register/")
    return render(request, "forum_posts/create.html", {"form": form})

def edit_post(request, id):
    if request.user.is_authenticated:
        Post_user = sell_post.objects.filter(id=id, Author=request.user)
        Item_fg = buyed_item.objects.filter(foring_key_sell_post=id)
        if Post_user.exists():
            Post_info = Post_user.get()
            Title = Post_info.Title
            Text = Post_info.Text
            Item_fg = Item_fg.get()
            ITem = Item_fg.Text
            Price = Post_info.Price
            tags = Post_info.tags.all()
            information_table = [Title, Text, Price, tags,ITem]
            if request.method == "POST":
                form = Create_Form(request.POST)
                if form.is_valid():
                    Title = form.cleaned_data["title"]
                    Tags = form.cleaned_data["tags"]
                    Price = form.cleaned_data["price"]
                    Item = form.cleaned_data["item"]
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
                    Post_user.update(Title=Title, Text=Message, Price=Price)
                    tags_list = [tag.strip() for tag in Tags.split(',')]
                    Post_user.get().tags.set(tags_list)
                    Item_fg.Text = Item
                    Item_fg.save()
                    return redirect("posts_sell:print_post")
            else:
                form = Create_Form(initial={"title": Title, "text": Text, "price": Price, "tags": ', '.join(str(tag) for tag in tags)})
            return render(request, "forum_posts/edit.html", {"information_table": information_table})
        else:
            return HttpResponse('Post not found or you are not the author.')
    else:
        return redirect("/register/")

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = sell_post.objects.filter(id=id, Author=request.user)
            if post.exists():
                post.delete()
                return redirect('posts_sell:print_post')
            else:
                return HttpResponse('Post not found or you are not the author.')
    else:
        return redirect("/register/")

def marketplace(request):
    if request.user.is_authenticated:
        Posts = sell_post.objects.filter(Post_status=3).order_by('Add_date')
        return render(request, "forum_posts/marketplace.html", {"Posts": Posts})
    else:
        return redirect("/register/")

def marketplace_one_product(request, id):
    if request.user.is_authenticated:
        Post = sell_post.objects.filter(id=id).get()
        print(Post)
        if Post:
            money = request.user.user_money
            return render(request, "forum_posts/marketplace_one_product.html", {"Post": Post,"money": money})
        else:
            return HttpResponse('Post not found.')
    else:
        return redirect("/register/")
    
def buy_product(request, id):
    if request.user.is_authenticated:
        Post = sell_post.objects.filter(id=id).get()
        if Post:
            if request.user == Post.Author:
                return HttpResponse('You cannot buy your own product.')
            if user_bought_items.objects.filter(foring_key_buy_item=Post, User=request.user):
                return HttpResponse('You have already purchased this product.')
            if request.user.user_money >= Post.Price:
                request.user.user_money -= Post.Price
                request.user.save()
                user_bought_items.objects.create(foring_key_buy_item=Post, User=request.user)
                CustomUser.objects.filter(id=Post.Author.id).update(user_money=Post.Author.user_money + Post.Price)
                return redirect("posts_sell:marketplace")
            else:
                return HttpResponse('Insufficient funds to complete the purchase.')
        else:
            return HttpResponse('Post not found.')
    else:
        return redirect("/register/")