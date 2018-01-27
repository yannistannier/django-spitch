from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'apps.authentication'
    verbose_name = 'Utilisateurs'

    def ready(self):
        import apps.authentication.signals  # noqa
