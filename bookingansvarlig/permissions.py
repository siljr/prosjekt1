from band_booking.models import Scene, Band
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_migrate
from django.contrib.auth import models as auth_models
from django.dispatch import receiver
from permission_creator import add_permissions_group


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds the Bookingansvarlig group and gives it the required permissions
    """
    add_permissions_group("Bookingansvarlig", [
        ("view_scenes", "Can see scenes information"),
    ])
