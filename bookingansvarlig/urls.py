from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from . import views

__author__ = 'Weronika'

urlpatterns = [
    url(r'^scenes$',
        permission_required('band_booking.view_scenes', login_url='/login')(views.ScenesListView.as_view()),
        name='scenes'),
    url(r'^scenes/(?P<scene>([A-Za-z 0-9]+))/$', views.concert_scene, name='concert_scene'),
    url(r'^info/(?P<concert>([A-Za-z 0-9]+))/$', views.band_info, name='concert_scene')
]
