from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from . import views


app_name = "bookingsjef"
urlpatterns = [
    url(r'^economy/concert/(?P<concert_id>([0-9]+))/$',permission_required('band_booking.view_concert_economic_results', login_url='/login')(views.economic_result_concert), name="economic_result"),
    url(r'^economy/price_generator/$', permission_required('band_booking.view_concert_economic_results', login_url='/login')(views.price_generator), name="price_generator")
]