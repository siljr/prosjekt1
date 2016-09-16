from django.db import models

__author__ = 'Weronika'


class Band(models.Model):
    name = models.CharField(max_length=128)
