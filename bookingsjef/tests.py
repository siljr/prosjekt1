from django.test import TestCase
from bookingsjef.algorithms.ticket_price import get_ticket_prices_for_scenes
from band_booking.models import Band, Scene


# Create your tests here.


class TicketPriceTest(TestCase):
    def setUp(self):
        Scene.objects.create(number_of_seats=200, expenditure=30000, scene_name=Scene.EDGAR)
        Scene.objects.create(number_of_seats=500, expenditure=100000, scene_name=Scene.STORSALEN)
        Scene.objects.create(number_of_seats=300, expenditure=65000, scene_name=Scene.KLUBBEN)
        Scene.objects.create(number_of_seats=200, expenditure=20000, scene_name=Scene.KNAUS)

    def test_get_ticket_prices_for_scenes(self):
        band = Band.objects.create(band_name='u2', genre='rock', booking_price=10000, streaming_numbers=100)
        data = get_ticket_prices_for_scenes(band.band_name, 50000)
        self.assertEqual(len(data), 4)

    def test_get_ticket_prices_for_scenes_wrong_band_name(self):
        band_name = "qwerettrytuy"
        data = get_ticket_prices_for_scenes(band_name, 50000)
        self.assertEqual(data, None)
