from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import permission_required


app_name = "bandmedlem"
urlpatterns = [
    url(r'^offers/band/$', views.band_offers, name='bookings'),
    url(r'^band/calendar/(?P<year>([0-9]{4}))/(?P<month>(([1][0-2]|[1-9]{1})))/$', permission_required('band_booking.can_view_band_calendar', login_url='/login')(views.concerts_band), name='calendar')
]
