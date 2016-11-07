from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Band, Booking, Technical_needs


# Create your tests here.

class BandMethodsTest(TestCase):
    """
    Test class for testing Band model class help methods
    """

    def setUp(self):
        """
        Method that initiates objects used in test methods
        """
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
        self.equipment = Technical_needs.objects.create(equipment_name='mic', amount=2, band=self.band)

    def test_get_bandmedlems_band(self):
        """
        Test of Band.get_bandmedlems_band() method whether it retrieves correct band form database based on user (bandmedlem)
        """
        band = Band.get_bandmedlems_band(self.bandmedlem)
        self.assertEqual(band, self.band)

    def test_get_band_manager_bookings(self):
        """
        Test of band.get_band_manager_bookings() method whether it retrieves correct bookings based on manager's email
        """
        booking = Booking.objects.create(title_name='booking', recipient_email=self.manager_mail)
        bookings = self.band.get_band_manager_bookings()
        self.assertEqual(bookings[0], booking)

    def test_equipment(self):
        """
        Test of band.equipment() method whether it retrieves correct band equipment based on user (bandmedlem)
        """
        band_equipment = Band.equipment(self.bandmedlem)
        self.assertEqual(band_equipment[0], self.equipment)
