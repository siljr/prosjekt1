from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models
from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from band_booking.models import Concert


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Arrangør to the user group list. Adds permission to this group for seeing concert information
    """
    group, created = auth_models.Group.objects.get_or_create(name='Arrangør')

    permission_can_view_concert_information, created = Permission.objects.get_or_create(
            codename='view_concert_information',
            name='Can view concert information',
            content_type=ContentType.objects.get_for_model(Concert)
    )

    group.permissions.add(permission_can_view_concert_information)