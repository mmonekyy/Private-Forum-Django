from django.shortcuts import render

# Create your views here.
def points(request):

    return render(request, 'points.html')

def ranks(request):

    return render(request, 'ranks.html')

def leaderboard(request):

    return render(request, 'leaderboard.html')
