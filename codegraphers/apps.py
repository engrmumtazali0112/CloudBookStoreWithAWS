from django.apps import AppConfig


class CodegraphersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'codegraphers'

    def ready(self):
        """Import signals when app is ready"""
        import codegraphers.signals