from django.apps import AppConfig


class BandmedlemConfig(AppConfig):
    name = 'bandmedlem'

    def ready(self):
        from .permissions import add_user_permissions
        try:
            add_user_permissions()
        except Exception as e:
            print(e)
