from django.shortcuts import render

# Create your views here.
def events(request):

    return render(request, 'forum_events/events.html')

def event(request, event_id):

    return render(request, 'forum_events/event.html', {'event_id': event_id})

