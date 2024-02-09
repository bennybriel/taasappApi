from django.apps import AppConfig


class TaasappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taasapp'
    # def ready(self):
    #     import taasapp.signals  # Add this line to import the signals.py