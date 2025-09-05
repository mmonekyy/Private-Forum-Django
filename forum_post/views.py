from django.shortcuts import render
from .forms import PostForm
from .models import ForumPost , Comment
from forum_users.models import CustomUser
from django.shortcuts import redirect
from django.utils import timezone

# Create your views here.
def create(request,category_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                tags = form.cleaned_data['tags']
                Author = request.user
                post = ForumPost.objects.create(
                    Title=title,
                    Content=content,
                    Category_id=category_id,
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
        tags = forum_data.tags.all()
        tags= ','.join([tag.name for tag in tags])
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                forum_data.Title = form.cleaned_data['title']
                forum_data.Content = form.cleaned_data['content']
                tags = form.cleaned_data['tags']
                tags_list = [tag.strip() for tag in tags.split(',')]
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
        own_posts = ForumPost.objects.filter(Author=request.user)
        return render(request, 'forum_post/own_posts.html',{"own_posts": own_posts})
    else:
        return redirect("/register/")
    
def view_all_posts(request):
    if request.user.is_authenticated:
        ForumPosts = ForumPost.objects.all().order_by('-Created_at')
        return render(request, 'forum_post/all_posts.html',{"ForumPosts": ForumPosts})
    else:
        return redirect("/register/")

def view_post(request, post_id):
    if request.user.is_authenticated:
        post = ForumPost.objects.get(id=post_id)
        comment = Comment.objects.filter(Post=post)
        return render(request, 'forum_post/view_post.html',{"post": post , "comments": comment})
    else:
        return redirect("/register/")

def add_comment(request, post_id):
    if request.user.is_authenticated:
        post = ForumPost.objects.get(id=post_id)
        if request.method == "POST":
            test = request.POST.get('comment')
            Comment.objects.create(
                Post=post,
                Author=request.user,
                Content=test,
            )
            return redirect("/Posts/Post/"+str(post_id)+"/")
    else:
        return redirect("/register/")