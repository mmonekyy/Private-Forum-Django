from django.shortcuts import render
from .forms import PostForm , serch
from .models import ForumPost , Comment , Category
from forum_users.models import CustomUser
from django.shortcuts import redirect
from django.utils import timezone
from django.http import HttpResponse
from django.core.paginator import Paginator

def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                tags = form.cleaned_data['tags']
                category_form = form.cleaned_data['category']
                category = Category.objects.filter(Name=category_form)
                if not category.exists():
                    return HttpResponse('Bad category')
                Author = request.user
                post = ForumPost.objects.create(
                    Title=title,
                    Content=content,
                    Category_id=category.get().id,
                    Author=Author
                )
                tags_list = [tag.strip() for tag in tags.split(',')]
                post.tags.set(tags_list)
                form = PostForm()              
        else:
            form = PostForm()
    else:
        return redirect("/register/")
    return render(request, 'forum_post/create.html',{"form": form})

def edit(request, post_id):
    if request.user.is_authenticated:
        forum_data = ForumPost.objects.filter(id=post_id, Author=request.user).get()
        if not forum_data:
            return redirect("/Posts/ViewOwnPosts/")
        tags = ','.join([tag.name for tag in forum_data.tags.all()])
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            tags_str = request.POST.get('tags', '')
            if title and content:
                forum_data.Title = title
                forum_data.Content = content
                tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                forum_data.tags.set(tags_list)
                forum_data.save()
                return redirect("/Posts/ViewOwnPosts/")
    else:
        return redirect("/register/")
    return render(request, 'forum_post/edit.html',{"form_data": forum_data, "tags": tags})

def delete(request, post_id):
    if request.user.is_authenticated:
        post = ForumPost.objects.get(id=post_id)
        if post.Author == request.user:
            post.delete()
            return redirect("/Posts/ViewOwnPosts/")
    else:
        return redirect("/register/")   

def view_own_post(request):
    if request.user.is_authenticated:
        own_posts = ForumPost.objects.filter(Author=request.user).order_by('-Created_at')
        paginator = Paginator(own_posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'forum_post/own_posts.html',{"own_posts": page_obj,"page_obj": page_obj})
    else:
        return redirect("/register/")
    
def view_all_posts(request):
    if request.user.is_authenticated:
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
        return render(request, 'forum_post/all_posts.html',{"ForumPosts": page_obj, "form": form,"query": request.GET.copy()})
    else:
        return redirect("/register/")

def view_post(request, post_id):
    if request.user.is_authenticated:
        post = ForumPost.objects.get(id=post_id)
        comment = Comment.objects.filter(Post=post)
        paginator = Paginator(comment, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'forum_post/view_post.html',{"post": post , "page_obj": page_obj})
    else:
        return redirect("/register/")

def add_comment(request, post_id):
    if request.user.is_authenticated:
        post = ForumPost.objects.get(id=post_id)
        if request.method == "POST":
            test = request.POST.get('comment')
            Comment.objects.create(Post=post,Author=request.user,Content=test)
            
            return redirect("view_post", post_id=post_id)
    else:
        return redirect("/register/")