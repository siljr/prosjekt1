from django.shortcuts import render
from django.views import generic
from band_booking.models import Concert


# Create your views here.

class ConcertsView(generic.ListView):
    template_name = 'arrangør/concert_overview.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        concerts = Concert.objects.filter(date__range=["2016-08-16", "2016-11-28"])
        return concerts
