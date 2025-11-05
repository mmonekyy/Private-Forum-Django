from django.shortcuts import render , redirect
from django.core.paginator import Paginator
from forum_posts_sell.models import sell_post
from forum_post.models import ForumPost , Category , Comment
from .forms import serch
def verfiy_mod(request):
    if not request.user.is_authenticated:
        return redirect("/register/")
    if request.user.is_mod() or request.user.is_head_mod():
        return None
    else:
        return redirect('/')

def check_post(request):
    response = verfiy_mod(request)
    if response:
        return response
    ForumPosts = ForumPost.objects.all().order_by('-Created_at')
    form = serch(request.GET or None)
    if form.is_valid():
        category = form.cleaned_data['category']
        tags = form.cleaned_data['tags']
        title = form.cleaned_data['title'] 
        if category:
            Category_id = Category.objects.filter(Name=category)
            if Category_id.exists():
                ForumPosts = ForumPosts.filter(Category_id=Category_id.get().id)
        if title:
            ForumPosts = ForumPosts.filter(Title__icontains=title)
        if tags:
            tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag in tags_list:
                ForumPosts = ForumPosts.filter(tags__name__in=[tag])
    else:
        form = serch()
    paginator = Paginator(ForumPosts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_panel/check_posts.html', {"ForumPosts": page_obj, "form": form,"query": request.GET.copy()})

def get_one_post(request, post_id):
    response = verfiy_mod(request)
    if response:
        return response
    post = ForumPost.objects.get(id=post_id)
    comment = Comment.objects.filter(Post=post)
    paginator = Paginator(comment, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_panel/one_post.html',{"post": post , "page_obj": page_obj})

def delete_comment(request, command_id):
    response = verfiy_mod(request)
    if response:
        return response
    comment = Comment.objects.get(id=command_id)
    comment.delete()
    return redirect('forum_post')

def delete_post(request, post_id):
    response = verfiy_mod(request)
    if response:
        return response
    post = ForumPost.objects.get(id=post_id)
    post.delete()
    return redirect('forum_post')

def modpanel(request):
    response = verfiy_mod(request)
    if response:
        return response
    username = request.user.username
    return render(request, 'admin_panel/modpanel.html', {'username':username})

def check_post_sell(request):
    response = verfiy_mod(request)
    if response:
        return response
    sell_posts = sell_post.objects.all().order_by('-Add_date').filter(Post_status=1,)
    paginator = Paginator(sell_posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_panel/check_posts_sell.html', {'page_obj': page_obj})

def get_one_post_sell(request, post_id):
    response = verfiy_mod(request)
    if response:
        return response
    post = sell_post.objects.get(id=post_id)
    return render(request, 'admin_panel/one_post_sell.html', {'post': post})

def approve_post_sell(request, post_id):
    response = verfiy_mod(request)
    if response:
        return response
    post = sell_post.objects.get(id=post_id)
    post.Post_status = 3
    post.save()
    return redirect('forum_sellpost')

def delete_post_sell(request, post_id):
    response = verfiy_mod(request)
    if response:
        return response
    post = sell_post.objects.get(id=post_id)
    post.delete()
    return redirect('forum_sellpost')


