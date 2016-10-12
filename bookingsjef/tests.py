from django.test import TestCase
from bookingsjef.algorithms.ticket_price import _get_marked_data
from band_booking.models import Band


# Create your tests here.


class TicketPriceTest(TestCase):
    def setUp(self):
        self.band = Band.objects.create(band_name='u2', genre='rock', booking_price=10000, streaming_numbers=100)

    def test_get_marked_data(self):
        data = _get_marked_data(self.band)
