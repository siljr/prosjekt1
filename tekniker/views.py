from django.shortcuts import render
from band_booking.models import Concert, Person
from django.contrib.auth.models import User
# Create your views here.

def tekniker_concerts(request):
    concerts = Concert.objects.filter(personnel=User.objects.get(user=request.user))
    context = {
        'concerts': concerts
    }
    return render(request, 'tekniker/myconcerts.html', context)