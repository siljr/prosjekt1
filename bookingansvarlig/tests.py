from django.test import TestCase
from band_booking.models import Booking
from django.contrib.auth.models import User
from django.core import mail
from .actions.send_booking import send_booking
from django.test.utils import override_settings

__author__ = 'Weronika'


# @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class SendBookingTest(TestCase):
    """
    Test class that checks if send_booking method sends mail correctly for booking object with status APPROVED and it
    raises ValueError if bookingn is not approved.

    Tests use mailbox "simulator" and don't send mails "for real". To send mail "for real" using gmail smtp server
    configured in settings comment out line 11 of this file (@override_settings.... , right above class declaration)
    and add real email for recipient_email parameter (in creation of Booking object in setUp() method). Run tests.
    Notice that some tests will fail then, but the email will be send "for real".

    Notice that gmail smtp server has some limit as to numbers of emails send per day (from 25-99?), so let's not overuse it.
    """

    def setUp(self):
        """
        Instantiates objects for testing
        """
        user = User.objects.create(email='fake_mail@fake.com')
        self.booking = Booking.objects.create(sender=user, title_name="mail_subject_test",
                                              recipient_email='fake_recipient@fake.com')

    def test_send_booking_approved(self):
        """
        Tests that send_booking returns True
        Tests that one message has been sent, with correct subject and body
        Tests that booking status has been updated
        """
        self.booking.status = Booking.APPROVED
        result = send_booking(self.booking)

        self.assertEqual(result, True)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(str(mail.outbox[0].subject), self.booking.title_name)
        self.assertEqual(str(mail.outbox[0].body), self.booking.email_text)

        new_status = Booking.objects.get(pk=self.booking.id).status
        self.assertEqual(new_status, Booking.SENT)

    def test_send_booking_not_approved(self):
        """
        Test that send_booking raises exception
        """
        self.booking.status = Booking.NOT_APPROVED
        with self.assertRaises(ValueError) as e:
            send_booking(self.booking)
        self.assertEqual(type(e.exception), ValueError)
