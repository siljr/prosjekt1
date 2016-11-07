from django.contrib.auth import models as auth_models
from django.db.models.signals import pre_migrate
from django.dispatch import receiver


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Bandmedlem to the user group list
    """
    group, created = auth_models.Group.objects.get_or_create(name='Bandmedlem')