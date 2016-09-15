from __future__ import unicode_literals
from datetime import date
from django.db import models

# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    telephone_number = models.IntegerField()
    email = models.CharField(max_length=50)
    related_name='a_person'

    ROLE_CHOICES = (
        ('MANAGER', 'manager'),
        ('ORGANIZER', 'organizer'),
        ('RIGGER', 'rigger'),
        ('CHIEF_ORGANIZER', 'chief organizer'),
        ('VOLUNTEER', 'volunteer'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='volunteer',
    )

    def __str__(self):
        return self.first_name+' '+self.last_name


class Album(models.Model):
    name = models.CharField(max_length=30)
    sales_numbers = models.IntegerField()
    related_name='an_album'

    def __str__(self):
        return self.name


class Scene(models.Model):
    number_of_seats=models.IntegerField()
    handicap_accessible=models.BooleanField
    related_name='a_scene'

    SCENE_CHOICES = (
        ('STORSALEN', 'storsalen'),
        ('KLUBBEN', 'klubben'),
        ('KNAUS', 'knaus'),
    )
    scene_name = models.CharField(
        max_length=20,
        choices=SCENE_CHOICES,
        default='storsalen',
    )

    def __str__(self):
        return self.scene_name
    def default(self):
        return 'storsalen'


class Band (models.Model,):
    band_name = models.CharField(max_length=30)
    manager = Person
    genre = models.CharField(max_length=20)
    albums = models.ManyToManyField(Album)
    booking_price = models.IntegerField()
    streaming_numbers = models.IntegerField()
    related_name="a_band"

    def __str__(self):
        return self.band_name


class Concert (models.Model):
    concert_title = models.CharField(max_length=50)
    date = models.DateField("Date", default=date.today())
    band = models.OneToOneField(
        Band,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    #band = models.OneToOneField(Band,default="Placeholder")
    #scene = models.OneToManyField(Scene,default='storsalen')
    personnel = models.ManyToManyField(Person)
    attendance = models.IntegerField()
    ticket_price = models.IntegerField()
    related_name='a_concert'

    STATUS_CHOICES = (
        ('BOOKED', 'Booked'),
        ('CONTACTED', 'Contacted'),
        ('PAID', 'Paid'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='contacted'
    )

    def __str__(self):
        return self.concert_title






