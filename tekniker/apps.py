from django.apps import AppConfig


class TeknikerConfig(AppConfig):
    name = 'tekniker'

    def ready(self):
        from .permissions import add_user_permissions
        try:
            add_user_permissions()
        except Exception as e:
            print(e)