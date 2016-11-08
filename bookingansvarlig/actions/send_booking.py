from django.core.mail import EmailMessage
from band_booking.models import Booking
from smtplib import SMTPException


def send_booking(booking: Booking):
    """
    Sends email with booking with info provided in booking parameter.
    Returns:
        bool: True if email was send successfully and False if it failed because of SMTPException
    Raises:
     ValueError: if booking is not approved.
    """
    if booking.status == Booking.APPROVED:
        email = EmailMessage(subject=booking.title_name, body=booking.email_text, to=[booking.recipient_email],
                             from_email=booking.sender.email)
        try:
            email.send(fail_silently=False)
            booking.change_status(Booking.SENT)
            return True
        except SMTPException:
            return False
    else:
        raise ValueError("Cannot send booking that does not have {0} status".format(Booking.APPROVED))
