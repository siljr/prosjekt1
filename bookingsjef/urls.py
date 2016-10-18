from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from . import views


app_name = "bookingsjef"
urlpatterns = [
    url(r'^economy/concert/(?P<concert_id>([0-9]+))/$',permission_required('band_booking.view_concert_economic_results', login_url='/login')(views.economic_result_concert), name="economic_result"),
    url(r'^booking/offer/approve/(?P<offer_id>([0-9]+))/$', permission_required('band_booking.can_approve_booking_offers', login_url='/login')(views.approve_booking_offer), {'approved': True}, name="approve_booking_offer"),
    url(r'^booking/offer/decline/(?P<offer_id>([0-9]+))/$', permission_required('band_booking.can_approve_booking_offers', login_url='/login')(views.approve_booking_offer), {'approved': False}, name="decline_booking_offer"),
    url(r'^booking/information/$', permission_required('band_booking.can_view_term_booking_information', login_url='/login')(views.booking_information_term), name='booking_information_term'),
]
