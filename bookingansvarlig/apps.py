
from django.apps import AppConfig

__author__ = 'Weronika'


class BookingansvarligConfig(AppConfig):
    name = 'bookingansvarlig'

    def ready(self):
        from .permissions import add_user_permissions
        add_user_permissions()
