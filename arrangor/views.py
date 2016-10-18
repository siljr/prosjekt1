from django.shortcuts import render
from django.views import generic
from band_booking.models import Concert


# Create your views here.

class ConcertsView(generic.ListView):
    template_name = 'arrangor/concert_overview.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        concerts = Concert.objects.all()
        return concerts
