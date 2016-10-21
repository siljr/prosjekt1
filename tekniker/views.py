from django.shortcuts import render
from band_booking.models import Concert
from django.contrib.auth.models import User
# Create your views here.

def tekniker_concerts(request):
    print(type(request))
    concerts = Concert.objects.filter(personnel=request.user)
    context = {
        'concerts': concerts
    }
    return render(request, 'tekniker/myconcerts.html', context)