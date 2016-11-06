from django.contrib.auth import models as auth_models
from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from permission_creator import add_permissions_group


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Arrangør to the group list
    """

    add_permissions_group("Arrangør", [
        ("view_concert_information", "Can view concert information"),
    ])