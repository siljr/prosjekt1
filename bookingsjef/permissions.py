from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_migrate
from django.contrib.auth import models as auth_models
from django.dispatch import receiver
from band_booking.models import Concert


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Bookingsjef to the group list
    """
    # Should add permissions for some content type.
    group, created = auth_models.Group.objects.get_or_create(name='Bookingsjef')
    content_type = ContentType.objects.get_for_model(Concert)
    permission, created_permission = Permission.objects.get_or_create(codename='view_concert_economic_results', name='Can see economic results for concerts',
                                     content_type=content_type)
    group.permissions.add(permission)



