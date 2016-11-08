from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models
from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from band_booking.models import Band


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Manager to the group list. Adds permission to this group for seeing technical needs information.
    """
    group, created = auth_models.Group.objects.get_or_create(name='Manager')

    permission_can_see_technical_requirements, created = Permission.objects.get_or_create(
            codename='see_technical_requirements',
            name='Can see technical requirements',
            content_type=ContentType.objects.get_for_model(Band)
    )

    group.permissions.add(permission_can_see_technical_requirements)
