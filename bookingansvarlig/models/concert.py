from django.db import models
from ..models.band import Band
from ..models.scene import Scene

__author__ = 'Weronika'


class Concert(models.Model):
    title = models.CharField(max_length=128)
    bands = models.ManyToManyField(Band)
    scenes = models.ManyToManyField(Scene)
