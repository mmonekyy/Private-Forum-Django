def check_user_type(request,sell_post, timezone, HttpResponse):
    if request.user.user_type == 1 and sell_post.objects.filter(Author=request.user, Add_date=timezone.now().date()).count() >= 1:
            return HttpResponse('You can only create one post per day.')
    if request.user.user_type == 2 and sell_post.objects.filter(Author=request.user, Add_date=timezone.now().date()).count() >= 4:
            return HttpResponse('You can only create four post per day.')
    if request.user.user_type == 3 and sell_post.objects.filter(Author=request.user, Add_date=timezone.now().date()).count() >= 6:
            return HttpResponse('You can only create six post per day.')
    if request.user.user_type == 4 and sell_post.objects.filter(Author=request.user, Add_date=timezone.now().date()).count() >= 2:
            return HttpResponse('You can only create two post per day.')
    if request.user.user_type == 5 and sell_post.objects.filter(Author=request.user, Add_date=timezone.now().date().count() >= 3):
            return HttpResponse('You can only create three post per day.')
    return None