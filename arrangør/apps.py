from django.apps import AppConfig


class ArrangørConfig(AppConfig):
    """
    Configures the app, setting the name and calling the permission setup
    """
    name = 'arrangør'

    def ready(self):
        from .permissions import add_user_permissions
        try:
            add_user_permissions()
        except Exception as e:
            print(e)
