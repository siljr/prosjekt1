from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import forms

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
    handicap_accessible = models.BooleanField()
    related_name = 'a_scene'

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
    attendance = models.IntegerField()
    ticket_price = models.IntegerField()
    related_name = 'a_concert'

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


class Booking(models.Model):

    sender = models.ForeignKey(User, null=True, blank=True)
    title_name = models.CharField(max_length=50,default = ' ')
    recipient_email = models.EmailField(max_length=50,default = ' ')
    email_text = models.CharField(max_length = 5000,default = 'Booking offer goes here')

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
    def __str__(self):
        return self.title_name

    def change_email_text(self, new_text):
        self.email_text = new_text
        self.save()

    def change_status(self, new_status):

        if new_status == 'U'| 'N'| 'A' | 'S':
            self.status = new_status
            self.save()







