from django.apps import AppConfig as DjangoAppConfig
from .signals import app_ready


class AppConfig(DjangoAppConfig):
    name = 'askbot'
    verbose_name = 'Askbot'

    def ready(self):
        app_ready.send(sender=self)
