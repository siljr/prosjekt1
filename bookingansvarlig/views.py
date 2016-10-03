from django.views import generic
from band_booking.models import Scene, Concert, Band
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
            'date': concert.date.strftime("%d.%m.%Y")
        }

    try:
        current_scene = Scene.objects.get(scene_name=scene)
    except ObjectDoesNotExist:
        return redirect('bookingansvarlig:scenes')
    concerts = Concert.objects.filter(scene=current_scene)

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
        'scene': scene,
    }




    return render(request, 'bookingansvarlig/concert_scene.html', context)


def create_booking_offer(request):
    return render(request, 'bookingansvarlig/create_booking_offer.html', {})
