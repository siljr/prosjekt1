from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from . import views


app_name = "bookingansvarlig"
urlpatterns = [
    url(r'^scenes$',
        permission_required('band_booking.view_scenes', login_url='/login')(views.ScenesListView.as_view()),
        name='scenes'),
    url(r'^concerts/$', views.concert, name='concerts'),
    url(r'^booking/offer/(?P<offer_id>([0-9]+))/$', views.create_booking_offer, name='create_booking_offer'),
    url(r'^booking/offer/$', views.create_booking_offer, name='create_booking_offer'),
    url(r'^booking/offer/save/(?P<offer_id>([0-9]+))/$', views.update_booking_offer, name='update_booking_offer'),
    url(r'^booking/offer/save/$', views.update_booking_offer, name='update_booking_offer'),
    url(r'^bookings$', views.BookingListView.as_view(), name='bookings'),
    url(r'^booking/create_offer$', views.create_booking_offer, name='create_booking_offer'),
]
