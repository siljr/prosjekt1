from django.db.models.signals import pre_migrate
from django.contrib.auth import models as auth_models
from django.dispatch import receiver
from permission_creator import add_permissions_group


@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(**kwargs):
    """
    Adds the Bookingsjef group and gives it the required permissions
    """

    add_permissions_group("Bookingsjef", [
        ("view_concert_economic_results", "Can see economic results for concerts"),
        ("view_all_booking_offers", "Can view all booking offers"),
        ("can_approve_booking_offers", "Can approve booking offers"),
        ("can_view_term_booking_information", "Can view term booking information"),
        ("can_create_booking", "Can create booking"),
    ])


