from django.core.mail import EmailMessage
from band_booking.models import Booking
from smtplib import SMTPException

__author__ = 'Weronika'


def send_booking(booking: Booking):
    # norwegian signs do not work
    if booking.status == Booking.APPROVED:
        email = EmailMessage(subject=booking.title_name, body=booking.email_text, to=booking.recipient_email,
                             from_email=booking.user.email)
        try:
            email.send(fail_silently=False)
            booking.change_status(Booking.SENT)
            return True
        except SMTPException:
            return False
    else:
        raise ValueError("Cannot send booking that does not have {0} status".format(Booking.APPROVED))
