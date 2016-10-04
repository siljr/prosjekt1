from django.views import generic
from band_booking.models import Scene, Concert, Band, Booking
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

__author__ = 'Weronika'


class ScenesListView(generic.ListView):
    """
    Retrieves list of all the scenes from database (ordered by scene_name) and renders scenes page.
    """
    template_name = 'bookingansvarlig/scenes_list.html'
    context_object_name = 'scenes_list'

    def get_queryset(self):
        scenes = Scene.objects.order_by('scene_name')
        return scenes


def concert_scene(request, scene):
    def build_concert(concert):
        return {
            'name': concert.concert_title,
            'bands': [band.band_name for band in concert.bands.all()],
            'date': concert.date.strftime("%d.%m.%Y"),
            'ticket_price': concert.ticket_price,
            'genre': [band.genre for band in concert.bands.all()],
            'attendance': concert.attendance,
            'scene': concert.scene.scene_name
        }

    try:
        current_scene = Scene.objects.all()
    except ObjectDoesNotExist:
        return redirect('bookingansvarlig:scenes')
    concerts = Concert.objects.all()

# Adds the serch functions
    query = request.GET.get('q')
    filteredConcerts = []
    for concert in concerts:
        if query:
            queryset_list = concert.bands.filter(band_name__icontains=query)
            if(queryset_list):
                filteredConcerts.append(concert)
        else:
            filteredConcerts.append(concert)

    context = {
        'concerts': [build_concert(concert) for concert in filteredConcerts],
    }

    return render(request, 'bookingansvarlig/concert_scene.html', context)


def create_booking_offer(request):
    return render(request, 'bookingansvarlig/create_booking_offer.html', {})


class BookingListView(generic.ListView):
    template_name = 'bookingansvarlig/bookings_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        bookings = Booking.objects.filter(sender=self.request.user)
        return bookings
