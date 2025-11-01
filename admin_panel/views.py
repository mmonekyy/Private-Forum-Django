from django.shortcuts import render , redirect
from django.core.paginator import Paginator
from forum_posts_sell.models import sell_post
def verfiy_mod(request):
    if request.user.is_mod or request.user.is_head_mod:
        pass
    else:
        redirect('forum_main')

def modpanel(request):
    verfiy_mod(request)
    username = request.user.username
    return render(request, 'admin_panel/modpanel.html', {'username':username})

def check_post_sell(request):
    verfiy_mod(request)
    sell_posts = sell_post.objects.all().order_by('-Add_date').filter(Post_status=1,)
    paginator = Paginator(sell_posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_panel/check_posts_sell.html', {'page_obj': page_obj})

def get_one_post_sell(request, post_id):
    verfiy_mod(request)
    post = sell_post.objects.get(id=post_id)
    return render(request, 'admin_panel/one_post_sell.html', {'post': post})

def approve_post_sell(request, post_id):
    verfiy_mod(request)
    post = sell_post.objects.get(id=post_id)
    post.Post_status = 3
    post.save()
    return redirect('forum_sellpost')

def delete_post_sell(request, post_id):
    verfiy_mod(request)
    post = sell_post.objects.get(id=post_id)
    post.delete()
    return redirect('forum_sellpost')

########################################################
def check_post(request):
    verfiy_mod(request)
    sell_posts = sell_post.objects.all().order_by('-Add_date').filter(Post_status=1,)
    paginator = Paginator(sell_posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_panel/check_posts.html', {'page_obj': page_obj})

def get_one_post(request, post_id):
    verfiy_mod(request)
    post = sell_post.objects.get(id=post_id)
    return render(request, 'admin_panel/one_post.html', {'post': post})

def delete_post(request, post_id):
    verfiy_mod(request)
    post = sell_post.objects.get(id=post_id)
    post.delete()
    post.save()
    return redirect('admin_panel:forum_sellpost')