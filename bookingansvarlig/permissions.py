from band_booking.models import Scene, Band
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_migrate
from django.contrib.auth import models as auth_models
from django.dispatch import receiver

__author__ = 'Weronika'


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Bookingansvarlig to the user group list. Adds permission to this group for seeing scenes information
    """
    auth_models.Group.objects.get_or_create(name='Bookingansvarlig')
    content_type = ContentType.objects.get_for_model(Scene)
    Permission.objects.get_or_create(codename='view_scenes', name='Can see scenes information',
                                     content_type=content_type)
