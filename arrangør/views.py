from django.shortcuts import render, redirect
from django.views import generic
from band_booking.models import Concert


# Create your views here.

class ConcertsView(generic.ListView):
    template_name = 'arrangør/concert_overview.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        concerts = Concert.objects.filter(date__range=["2016-08-16", "2016-11-28"])
        return concerts


def overview_concert(request, id):
    try:
        concert = Concert.objects.get(pk=id)
    except Concert.DoesNotExist:
        return redirect('arrangør:concerts')

    if not request.user.is_superuser and request.user != concert.organizer:
        return redirect('arrangør:concerts')

    return render(request, 'arrangør/concert.html', {'concert': concert})
