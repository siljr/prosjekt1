from django.shortcuts import render
from django.views import generic
from bookingansvarlig.models import Scene

__author__ = 'Weronika'


class ScenesListView(generic.ListView):
    template_name = 'bookingansvarlig/scenes_list.html'
    context_object_name = 'scenes_list'

    def get_queryset(self):
        scenes = Scene.objects.order_by('name')
        print(scenes)
        return scenes
