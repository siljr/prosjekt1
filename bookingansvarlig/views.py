from django.views import generic
from band_booking.models import Scene, Concert, Band
from django.shortcuts import render


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
    all_concerts = Concert.objects.filter()
    context = {
        'all_concerts': all_concerts,
        'scene': scene,
    }
    return render(request, 'bookingansvarlig/concert_scene.html', context)

def band_info(request, concert):
    context ={
        'concert': concert
    }
    return render(request, 'bookingansvarlig/info_concert.html', context)