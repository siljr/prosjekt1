from django.test import TestCase
from .actions.send_booking import send_booking
from django.test.utils import override_settings

__author__ = 'Weronika'

@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')

class SendBookingTest(TestCase):
    def setUp(self):
        pass

    def test_send_offer(self):
        send_booking('adress')



