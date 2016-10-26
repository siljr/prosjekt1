from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Band, Technical_needs

class BandTest(TestCase):
    def setUp(self):
        self.bandmedlem = User.objects.create_user(username='bandmedlem')
        g = Group.objects.create(name='Bandmedlem')
        g.user_set.add(self.bandmedlem)
        self.band = Band.objects.create(band_name='asda', genre='sad', booking_price=1, streaming_numbers=1)
        self.band.band_member.add(self.bandmedlem)
        self.equipment = Technical_needs.objects.create(equipment_name='mic', amount=2, band=self.band)

    def test_f(self):
        band_equipment=Band.equipment(self.bandmedlem)
        self.assertEqual(band_equipment[0], self.equipment)