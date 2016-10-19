from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = 'manager'

    def ready(self):
        from .permissions import add_user_permissions
        try:
            add_user_permissions()
        except Exception as e:
            print(e)

