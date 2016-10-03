from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from . import views


app_name = "bookingansvarlig"
urlpatterns = [
    url(r'^scenes$',
        permission_required('band_booking.view_scenes', login_url='/login')(views.ScenesListView.as_view()),
        name='scenes'),
    url(r'^scenes/(?P<scene>([A-Za-z 0-9]+))/$', views.concert_scene, name='concert_scene'),
    url(r'^booking/create_offer$', views.create_booking_offer, name='create_booking_offer'),
]
