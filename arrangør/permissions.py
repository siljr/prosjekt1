from django.contrib.auth import models as auth_models
from django.db.models.signals import pre_migrate
from django.dispatch import receiver


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Bookingsjef to the group list, and adds several permissions to the bookingsjef group
    """
    group, created = auth_models.Group.objects.get_or_create(name='Arrangør')