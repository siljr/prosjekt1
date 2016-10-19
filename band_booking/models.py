from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    telephone_number = models.IntegerField()
    email = models.EmailField()
    related_name = 'a_person'

    #adding choice variables helps to avoid typos and inconsistencies in the future
    #instead of using strings choices are easily available through class: Person.MANAGER
    MANAGER = 'M'
    ORGANIZER = 'O'
    RIGGER = 'R'
    CHIEF_ORGANIZER = 'C'
    VOLUNTEER = 'V'

    ROLE_CHOICES = (
        (MANAGER, 'manager'),
        (ORGANIZER, 'organizer'),
        (RIGGER, 'rigger'),
        (CHIEF_ORGANIZER, 'chief organizer'),
        (VOLUNTEER, 'volunteer'),
    )
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default=VOLUNTEER,
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Scene(models.Model):
    number_of_seats = models.IntegerField()
    handicap_accessible = models.NullBooleanField()
    related_name = 'a_scene'
    expenditure = models.IntegerField(default=0)

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
    band_name = models.CharField(max_length=30)
    manager = models.ForeignKey(Person, limit_choices_to={'role': Person.MANAGER}, null=True, blank=True)
    genre = models.CharField(max_length=20)
    booking_price = models.IntegerField()
    streaming_numbers = models.IntegerField()
    related_name = "a_band"

    def __str__(self):
        return self.band_name


class Album(models.Model):
    name = models.CharField(max_length=30)
    sales_numbers = models.IntegerField()
    band = models.ForeignKey(Band, null=True, blank=True)  # an album belongs to one band, but band can have many albums. Could be also ManyToManyField if album can have more then one band
    related_name = 'an_album'

    def __str__(self):
        return self.name


class Concert(models.Model):
    concert_title = models.CharField(max_length=50)
    date = models.DateField() #got en error with default=date.today() when migrating, so it's been removed
    bands = models.ManyToManyField(Band)  # There can play many bands on the concert and band can play many concerts
    scene = models.ForeignKey(Scene, null=True, blank=True)  # only one scene per concert, but many concerts per scene
    personnel = models.ManyToManyField(Person)
    attendance = models.IntegerField(default=0)
    ticket_price = models.IntegerField(default=0)
    booking_price = models.IntegerField(default=0)
    organizer = models.ForeignKey(User, limit_choices_to={'groups': "Arrangør"})
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
    )

    def __str__(self):
        return self.concert_title

    #Calculates the concert's economic result
    def calc_econ_result(self):
        return self.ticket_price*self.attendance-self.booking_price-self.scene.expenditure-self.GUARD_EXPENSE

    #Disguises the method call as a field
    @property
    def economic_result(self):
        return self.calc_econ_result()


class Booking(models.Model):
    EMAIL_MAX_LENGTH = 5000

    sender = models.ForeignKey(User, null=True, blank=True)
    title_name = models.CharField(max_length=50,default = ' ')
    recipient_email = models.EmailField(max_length=50,default = ' ')
    email_text = models.CharField(max_length = EMAIL_MAX_LENGTH,default = 'Booking offer goes here')

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
        default ='U',
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
        status_words = {'U': 'Under godkjenning', 'N': 'Ikke godkjent', 'A': 'Godkjent', 'S': 'Sent'}
        return status_words[self.status]

    def user_allowed_to_view(self, user):
        """
        Checks if the given user is allowed to view the booking offer
        """
        return self.sender == user or user.has_perm('band_booking.view_all_booking_offers')

    def __str__(self):
        return self.title_name


    # Unused change method for changing e-mail text.
    #def change_email_text(self, new_text):
    #    if len(new_text) < self.EMAIL_MAX_LENGTH:
    #        self.email_text = new_text
    #        self.save()

    def change_status(self, new_status): #Method that changes the status of the booking
        if new_status in (Booking.UNDECIDED, Booking.NOT_APPROVED, Booking.APPROVED, Booking.SENT):
            self.status = new_status
            self.save()


@receiver(models.signals.post_save, sender=Booking)
def handle_change(sender, **kwargs):
    """
    Sends the email for the booking offer when the status changes to approved
    """
    booking_object = kwargs['instance']
    if booking_object.status == Booking.APPROVED:
        from bookingansvarlig.actions.send_booking import send_booking
        send_booking(booking_object)
        booking_object.change_status(Booking.SENT)







