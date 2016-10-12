from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_migrate
from django.contrib.auth import models as auth_models
from django.dispatch import receiver
from band_booking.models import Concert, Booking


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds Bookingsjef to the group list, and adds several permissions to the bookingsjef group
    """
    group, created = auth_models.Group.objects.get_or_create(name='Bookingsjef')
    permission_can_view_economic_results, created = Permission.objects.get_or_create(
            codename='view_concert_economic_results',
            name='Can see economic results for concerts',
            content_type=ContentType.objects.get_for_model(Concert)
    )

    permission_can_view_all_booking_offers, created = Permission.objects.get_or_create(
        codename='view_all_booking_offers',
        name='Can view all booking offers',
        content_type=ContentType.objects.get_for_model(Booking)
    )

    permission_can_approve_booking_offers, created = Permission.objects.get_or_create(
        codename='can_approve_booking_offers',
        name='Can approve booking offers',
        content_type=ContentType.objects.get_for_model(Booking),
    )

    group.permissions.add(permission_can_approve_booking_offers)
    group.permissions.add(permission_can_view_economic_results)
    group.permissions.add(permission_can_view_all_booking_offers)



