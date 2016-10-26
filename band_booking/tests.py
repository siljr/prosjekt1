from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Band, Booking


# Create your tests here.

class BandMethodsTest(TestCase):
    def setUp(self):
        self.bandmedlem = User.objects.create_user(username='bandmedlem')
        g = Group.objects.create(name='Bandmedlem')
        g.user_set.add(self.bandmedlem)
        self.manager_mail = "manager@her.no"
        self.manager = User.objects.create_user(username='manager', email=self.manager_mail)
        g2 = Group.objects.create(name='Manager')
        g2.user_set.add(self.manager)
        self.band = Band.objects.create(band_name='bla', manager=self.manager, booking_price=100, genre='jazz',
                                        streaming_numbers=111)
        self.band.band_member.add(self.bandmedlem)

    def test_get_bandmedlems_band(self):
        band = Band.get_bandmedlems_band(self.bandmedlem)
        self.assertEqual(band, self.band)

    def test_get_band_manager_bookings(self):
        booking = Booking.objects.create(title_name='booking', recipient_email=self.manager_mail)
        bookings = self.band.get_band_manager_bookings()
        self.assertEqual(bookings[0], booking)
