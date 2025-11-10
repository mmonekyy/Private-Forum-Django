from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from forum_posts_sell.models import sell_post
from forum_post.models import ForumPost
from django.utils import timezone
from datetime import timedelta

def forum_main(request):
    if not request.user.is_authenticated:
        return redirect("/register/")

    thirty_days_ago = timezone.now() - timedelta(days=30)

    best_rated_posts = (
        sell_post.objects.filter(Post_status=3, Add_date__gte=thirty_days_ago)
        .annotate(
            avg_rating=Avg('opinion__Rate'),
            rating_count=Count('opinion')
        )
        .filter(avg_rating__isnull=False)
        .order_by('-avg_rating')[:5]
    )

    worst_rated_posts = (
        sell_post.objects.filter(Post_status=3, Add_date__gte=thirty_days_ago)
        .annotate(
            avg_rating=Avg('opinion__Rate'),
            rating_count=Count('opinion')
        )
        .filter(avg_rating__isnull=False)
        .order_by('avg_rating')[:5]
    )
    latest_posts = ForumPost.objects.all().order_by('-Created_at')[:5]

    context = {
        'best_rated_posts': best_rated_posts,
        'worst_rated_posts': worst_rated_posts,
        'latest_posts': latest_posts,
    }
    return render(request, 'forum/forum.html', context)
