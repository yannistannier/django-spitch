from django.apps import AppConfig


class AskConfig(AppConfig):
    name = 'apps.ask'

    def ready(self):
        import apps.ask.signals  # noqa
