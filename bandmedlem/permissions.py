from django.contrib.auth import models as auth_models
from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from permission_creator import add_permissions_group


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Bandmedlem as a group and gives the group the required permissions
    """

    add_permissions_group("Bandmedlem", [
        ('can_view_band_calendar', 'Can view band calendar'),
        ('can_view_band_offers', 'Can view band offers'),
    ])