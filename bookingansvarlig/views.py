from django.views import generic
from band_booking.models import Scene, Concert, Band
from django.shortcuts import render, redirect
from django.utils import timezone
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


def concert(request):
    def build_concert(concert):
        """
        Builds the information about a concert from the concert model
        """
        return {
            'pk': concert.pk,
            'name': concert.concert_title,
            'bands': [band.band_name for band in concert.bands.all()],
            'date': concert.date.strftime("%d.%m.%Y"),
            'ticket_price': concert.ticket_price,
            'genre': [band.genre for band in concert.bands.all()],
            'attendance': concert.attendance,
            'scene': concert.scene.scene_name,
        }

    def get_genres(concerts):
        """
        Finds all possible genres from bands that have played at Samfundet
        """
        genres = []
        for concert in concerts:
            for band in concert.bands.all():
                if band.genre not in genres:
                    genres.append(band.genre)
        return genres

    concerts = Concert.objects.all()

    # Adds the search functions
    band_name_query, genre_query, scene_query = request.GET.get('band_name', ''), request.GET.get('genre', ''), request.GET.get('scene', '')
    filtered_concerts = []
    for concert in concerts.filter(scene__scene_name__icontains=scene_query).filter(date__lte=timezone.now()).order_by('-date'):
        queryset_list = concert.bands.filter(band_name__icontains=band_name_query).filter(genre__icontains=genre_query)
        if queryset_list:
            filtered_concerts.append(concert)

    context = {
        'genres': get_genres(concerts),
        'concerts': [build_concert(concert) for concert in filtered_concerts],
        'genre': genre_query,
        'scene': scene_query,
        'band_name': band_name_query,
        'scenes': [scene.scene_name for scene in Scene.objects.all()]
    }

    return render(request, 'bookingansvarlig/concert_scene.html', context)


def create_booking_offer(request):
    return render(request, 'bookingansvarlig/create_booking_offer.html', {})
