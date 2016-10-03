from django.test import TestCase
from band_booking.models import Booking
from django.contrib.auth.models import User
from django.core import mail
from .actions.send_booking import send_booking
from django.test.utils import override_settings

__author__ = 'Weronika'


# @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class SendBookingTest(TestCase):
    def setUp(self):
        user = User.objects.create(email='user_email@qqq.com')
        self.booking = Booking.objects.create(sender=user, title_name="mail_subject_test",
                                              recipient_email='recipient@qqq.com')

    def test_send_booking_approved(self):
        self.booking.status = Booking.APPROVED
        result = send_booking(self.booking)
        self.assertEqual(result, True)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(str(mail.outbox[0].subject), self.booking.title_name)
        self.assertEqual(str(mail.outbox[0].body), self.booking.email_text)
        # Test that booking status has been updated
        new_status = Booking.objects.get(pk=self.booking.id).status
        self.assertEqual(new_status, Booking.SENT)

    def test_send_booking_not_approved(self):
        self.booking.status = Booking.NOT_APPROVED
        result = send_booking(self.booking)