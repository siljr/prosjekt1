from django.shortcuts import render
from django.views import generic
from band_booking.models import Booking, Band


def band_offers(request):
    pass


class BandListView(generic.ListView):
    template_name = 'bandmedlem/view_for_offers.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return [booking for booking in Booking.objects().filter()]

