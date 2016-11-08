from django.shortcuts import render
from band_booking.models import Concert
from datetime import datetime


def tekniker_concerts(request):
    """
    Renders page with concerts overview for the user (tekniker)
    """
    concerts = Concert.objects.filter(personnel=request.user, date__gte=datetime.now())
    context = {}
    if concerts:
        context['concerts'] = concerts
    return render(request, 'tekniker/myconcerts.html', context)