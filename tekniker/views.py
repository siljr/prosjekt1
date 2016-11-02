from django.shortcuts import render
from band_booking.models import Concert
from datetime import datetime
from django.contrib.auth.models import User
# Create your views here.

def tekniker_concerts(request):
    concerts = Concert.objects.filter(personnel=request.user, date__gte=datetime.now())
    context = {}
    if concerts:
        context['concerts'] = concerts
    return render(request, 'tekniker/myconcerts.html', context)