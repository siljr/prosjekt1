from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_migrate
from django.contrib.auth import models as auth_models
from django.dispatch import receiver


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Bookingsjef to the group list
    """
    # Should add permissions for some content type.
    auth_models.Group.objects.get_or_create(name='Bookingsjef')
