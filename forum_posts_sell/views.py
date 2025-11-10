from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import Create_Form , Opinion
from .models import sell_post , buyed_item , user_bought_items , opinion
from .support_function_views import check_user_type
from forum_users.models import CustomUser
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import serch_Form

def marketplace(request):
    if request.user.is_authenticated:
        Posts = sell_post.objects.filter(Post_status=3).order_by('Add_date')

        form = serch_Form(request.GET or None) 
        if form.is_valid():
            tags = form.cleaned_data['tag']
            title = form.cleaned_data['title'] 
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            author = form.cleaned_data['author']
            if title:
                Posts = Posts.filter(Title__icontains=title)
            if tags:
                tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
                for tag in tags_list:
                    Posts = Posts.filter(tags__name__in=[tag])
            if min_price is not None:
                Posts = Posts.filter(Price__gte=min_price)
            if max_price is not None and max_price > 0:
                Posts = Posts.filter(Price__lte=max_price)
            if author:
                Posts = Posts.filter(Author__username__icontains=author)
        else:
            form = serch_Form() 

        paginator = Paginator(Posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "forum_posts/marketplace.html", {"Posts": page_obj,"form":form})
    else:
        return redirect("/register/")

def print_post(request):
    if request.user.is_authenticated:
        user_posts = sell_post.objects.filter(Author=request.user)
        paginator = Paginator(user_posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        return redirect("/register/")
    return render(request,"forum_posts/print.html",{"page_obj":page_obj,})

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
                error = None
                if Price < 0:
                    error = "Price cannot be negative"
                elif len(Title) < 5:
                    error = "Title is too short"
                elif len(Title) > 100:
                    error = "Title is too long"
                elif len(Tags) > 50:
                    error = "Tags are too long"
                elif len(Tags) < 3:
                    error = "Tags are too short"
                    
                if error:
                    return render(request, "forum_posts/create.html", {"form": form, "error": error})
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
                    error = None
                    if Price < 0:
                        error = "Price cannot be negative"
                    elif len(Title) < 5:
                        error = "Title is too short"
                    elif len(Title) > 100:
                        error = "Title is too long"
                    elif len(Tags) > 50:
                        error = "Tags are too long"
                    elif len(Tags) < 3:
                        error = "Tags are too short"
                        
                    if error:
                        return render(request, "forum_posts/edit.html", {
                            "form": form, 
                            "error": error,
                            "information_table": information_table
                        })
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
            return render(request, "forum_posts/error.html", {"error_message": "Post not found or you are not the author."})
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
                return render(request, "forum_posts/error.html", {"error_message": "Post not found or you are not the author."})
    else:
        return redirect("/register/")


def marketplace_one_product(request, id):
    if request.user.is_authenticated:
        Post = sell_post.objects.filter(id=id,Post_status=3).get()
        if Post:
            money = request.user.user_money
            return render(request, "forum_posts/marketplace_one_product.html", {"Post": Post,"money": money})
        else:
            return render(request, "forum_posts/error.html", {"error_message": "Post not found."})
    else:
        return redirect("/register/")
    
def buy_product(request, id):
    if request.user.is_authenticated:
        Post = sell_post.objects.filter(id=id).get()
        buyed_item_fg = buyed_item.objects.filter(foring_key_sell_post=id).get()
        if Post:
            if request.user == Post.Author:
                return render(request, "forum_posts/error.html", {"error_message": "You cannot buy your own product."})
            if user_bought_items.objects.filter(foring_key_buy_item=buyed_item_fg, User=request.user):
                return render(request, "forum_posts/error.html", {"error_message": "You have already purchased this product."})
            if request.user.user_money >= Post.Price:
                request.user.user_money -= Post.Price
                request.user.save()
                user_bought_items.objects.create(foring_key_buy_item=buyed_item_fg, User=request.user)
                CustomUser.objects.filter(id=Post.Author.id).update(user_money=Post.Author.user_money + Post.Price)
                return redirect("posts_sell:marketplace")
            else:
                return render(request, "forum_posts/error.html", {"error_message": "Insufficient funds to complete the purchase."})
        else:
            return render(request, "forum_posts/error.html", {"error_message": "Post not found."})
    else:
        return redirect("/register/")
    
def user_items(request):
    if request.user.is_authenticated:
        user = request.user
        items = user_bought_items.objects.filter(User=user).select_related("foring_key_buy_item")
        paginator = Paginator(items, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "forum_posts/user_item.html", {"items": items})
    else:
        return redirect("/register/")
    
def item_detail(request, id):
    if not request.user.is_authenticated:
        return redirect("/register/")

    user = request.user
    try:
        item = user_bought_items.objects.select_related("foring_key_buy_item").get(User=user, id=id)
        post_rate = sell_post.objects.filter(
            buyed_item__user_bought_items__User=user,
            buyed_item__user_bought_items__id=id
        ).get()
        form = Opinion()
        message = None

        if request.method == "POST":
            opinionn = opinion.objects.filter(Author=user, foring_key_buy_item=post_rate)
            if opinionn.exists():
                message = "You have already rated this item."
            else:
                form = Opinion(request.POST)
                if form.is_valid():
                    rate = form.cleaned_data["rate"]
                    if rate < 1 or rate > 5:
                        message = "Rate must be between 1 and 5."
                    else:
                        opinion.objects.create(
                            foring_key_buy_item=post_rate,
                            Author=request.user,
                            Rate=rate
                        )
                        message = "Your rating has been saved."
        else:
            form = Opinion()

        return render(
            request,
            "forum_posts/item_detail.html",
            {"item": item, "form": form, "post_rate": post_rate, "message": message},
        )

    except user_bought_items.DoesNotExist:
        return redirect("posts_sell:user_items")
