from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.

class Scene(models.Model):
    """
    Class representing scene.
    """
    number_of_seats = models.IntegerField()
    handicap_accessible = models.NullBooleanField()
    related_name = 'a_scene'
    expenditure = models.IntegerField(default=0)

    # All the choices for the scenes
    STORSALEN = 'Storsalen'
    KLUBBEN = 'Klubben'
    KNAUS = 'Knaus'
    EDGAR = 'Edgar'

    SCENE_CHOICES = (
        (STORSALEN, 'storsalen'),
        (KLUBBEN, 'klubben'),
        (KNAUS, 'knaus'),
        (EDGAR, 'edgar')
    )
    scene_name = models.CharField(
        max_length=16,
        choices=SCENE_CHOICES,
        default=STORSALEN,
    )

    def __str__(self):
        return self.scene_name


class Band(models.Model):
    """
    Class representing band.
    """
    band_name = models.CharField(max_length=30)
    manager = models.OneToOneField(User, limit_choices_to={'groups__name': "Manager"}, null=True, blank=True)
    genre = models.CharField(max_length=20)
    band_member = models.ManyToManyField(User, limit_choices_to={'groups__name': "Bandmedlem"}, related_name='band_member', blank=True)
    booking_price = models.IntegerField(default=0)
    streaming_numbers = models.IntegerField(default=0)

    related_name = "a_band"

    def __str__(self):
        return self.band_name

    def get_band_manager_bookings(self):
        """
        :return: Returns all bookings sent to the manager of the band. Else raises an error.
        Raises:
            ValueError: if band's manager doesn't have an email
        """

        try:
            manager_email = self.manager.email
        except:
            raise ValueError("Manager's email missing")
        return Booking.objects.filter(recipient_email=manager_email)

    @classmethod
    def get_users_band(cls, user: User):
        """
        :param user: The user
        :return: The band the user is a member of if it exists
        """
        try:
            return Band.objects.filter(band_member=user)[:1].get()
        except Band.DoesNotExist:
            return None

    @classmethod
    def equipment(cls, user: User):
        """
        :param user: The user for which we want to find equipment needed
        :return: The equipment needed for the band of the user, if the user is a member of a band.
        """
        user_band = Band.objects.filter(band_member=user)[0]
        return Technical_needs.objects.filter(band=user_band)


class Concert(models.Model):
    """
    Class representation of concert.
    """
    concert_title = models.CharField(max_length=50)
    date = models.DateField()  # got en error with default=date.today() when migrating, so it's been removed
    bands = models.ManyToManyField(Band)  # There can play many bands on the concert and band can play many concerts
    scene = models.ForeignKey(Scene, null=True, blank=True)  # only one scene per concert, but many concerts per scene
    personnel = models.ManyToManyField(User, blank=True)
    attendance = models.IntegerField(default=0)
    ticket_price = models.IntegerField(default=0)
    booking_price = models.IntegerField(default=0)
    organizer = models.ForeignKey(User, limit_choices_to={'groups__name': 'Arrangør'}, null=True, blank=True, related_name='organizer')
    related_name = 'a_concert'

    GUARD_EXPENSE = 1000
    BOOKED = 'B'
    CONTACTED = 'C'
    PAID = 'P'

    STATUS_CHOICES = (
        (BOOKED, 'Booked'),
        (CONTACTED, 'Contacted'),
        (PAID, 'Paid'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=BOOKED
    )

    def __str__(self):
        return self.concert_title

    def calc_econ_result(self):
        """
        :return: The economic results for the concert
        Calculates the concert's economic result
        """
        return self.ticket_price * self.attendance - self.booking_price - self.scene.expenditure - self.GUARD_EXPENSE

    #
    @property
    def economic_result(self):
        """
        :return: The economic results for the concert
        The economic results for the concert disguised as a field.
        """
        return self.calc_econ_result()


class Technical_needs(models.Model):
    """
    Class representing specific technical needs for the band
    """
    equipment_name = models.CharField(max_length=128, default=' ')
    amount = models.IntegerField(default=1)
    band = models.ForeignKey(Band)

    def __str__(self):
        return self.equipment_name


class Booking(models.Model):
    """
    Class representing band booking.
    """

    EMAIL_MAX_LENGTH = 5000

    sender = models.ForeignKey(User, limit_choices_to={'groups__name': 'Bookingansvarlig'}, null=True, blank=True)
    title_name = models.CharField(max_length=50, default=' ')
    recipient_email = models.EmailField(max_length=50, default=' ')
    email_text = models.CharField(max_length=EMAIL_MAX_LENGTH, default='Booking offer goes here')
    date = models.DateField(default=timezone.now)
    scene = models.ForeignKey(Scene, null=True, blank=True, default=True)

    UNDECIDED = 'U'
    NOT_APPROVED = 'N'
    APPROVED = 'A'
    SENT = 'S'

    STATUS_CHOICES = (
        (UNDECIDED, 'Undecided'),
        (NOT_APPROVED, 'Not approved'),
        (APPROVED, 'Approved'),
        (SENT, 'Sent'),
    )
    status = models.CharField(
        default='U',
        max_length=1,
        choices=STATUS_CHOICES,
    )

    def get_status_message(self):
        """
        Returns a status message in Norwegian for the current status of the booking offer.
        """
        return "Tilbudet er " + self.get_status_word().lower()

    def get_status_word(self):
        """
        Returns a status word in Norwegian for the current status of the booking offer
        """
        status_words = {'U': 'Under godkjenning', 'N': 'Ikke godkjent', 'A': 'Godkjent', 'S': 'Sendt'}
        return status_words[self.status]

    def user_allowed_to_view(self, user):
        """
        Checks if the given user is allowed to view the booking offer
        """
        return self.sender == user or user.has_perm('band_booking.view_all_booking_offers')

    def __str__(self):
        return self.title_name

    def change_status(self, new_status):
        """
        :param new_status: The new status of the booking
        :return: None
        Changes the status of the booking to the new_status
        """
        if new_status in (Booking.UNDECIDED, Booking.NOT_APPROVED, Booking.APPROVED, Booking.SENT):
            self.status = new_status
            self.save()


@receiver(models.signals.post_save, sender=Booking)
def handle_change(sender, **kwargs):
    """
    :param sender: The sender of the Django signal
    :param kwargs: Keyword arguments for the give Django signal
    :return: None
    Sends an email for the given booking that had a change if the stauts was changed to approved.
    """
    booking_object = kwargs['instance']
    if booking_object.status == Booking.APPROVED:
        from bookingansvarlig.actions.send_booking import send_booking
        send_booking(booking_object)
        booking_object.change_status(Booking.SENT)
