from django.apps import AppConfig


class BookingsjefConfig(AppConfig):
    name = 'bookingsjef'

    def ready(self):
        from .permissions import add_user_permissions
        try:
            add_user_permissions()
        except Exception:
            pass
