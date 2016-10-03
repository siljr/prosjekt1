from django.test import TestCase
from .actions.send_offer import send_offer
from django.test.utils import override_settings

__author__ = 'Weronika'

@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class SendOfferTest(TestCase):
    def test_send_offer(self):
        print('test')
        send_offer('adress')



