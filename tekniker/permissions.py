from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_migrate
from django.contrib.auth import models as auth_models
from django.dispatch import receiver
from band_booking.models import Concert, Booking


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Tekniker to the group list, and adds several permissions to the tekniker group
    """
    group, created = auth_models.Group.objects.get_or_create(name='Tekniker')