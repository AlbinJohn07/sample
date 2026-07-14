from django.apps import AppConfig


class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app1'
    def ready(self):
        """Import signals when Django starts"""
        import app1.signals