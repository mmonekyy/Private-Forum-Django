from django.shortcuts import render
from .forms import PostForm
from .models import ForumPost
from forum_users.models import CustomUser
from django.shortcuts import redirect

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
    pass

def delete(request, post_id):
    pass

def view_own_post(request):
    pass

def view_all_posts(request):
    pass

def view_post(request, post_id):
    pass
