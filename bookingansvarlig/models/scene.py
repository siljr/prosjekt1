from django.db import models


__author__ = 'Weronika'


class Scene(models.Model):
    name = models.CharField(max_length=128)
    street_name = models.CharField(max_length=128, null=True, blank=True)  #don't know if info about address needed
    street_number = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    seats_number = models.SmallIntegerField()

    #availability
    #price


