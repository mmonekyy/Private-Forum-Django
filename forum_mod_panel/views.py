from django.shortcuts import render

# Create your views here.
def mod_panel(request):

    return render(request, 'forum_mod_panel/moderator.html')

def head_mod_panel_(request):
    
    return render(request, 'forum_mod_panel/headmoderator.html')