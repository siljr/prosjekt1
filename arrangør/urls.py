from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import permission_required


app_name = "arrangør"
urlpatterns = [
     url(r'^concerts_in_semester/$', permission_required('band_booking.view_concerts_term', login_url="/login")(views.ConcertsView.as_view()), name='concerts'),
     url(r'^concert/(?P<id>([0-9]+))', permission_required('band_booking.view_concert_information', login_url='/login')(views.overview_concert), name='concert'),
]
