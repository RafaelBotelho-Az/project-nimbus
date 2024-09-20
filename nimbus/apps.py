from django.apps import AppConfig


class NimbusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nimbus'

    def ready(self):
        import nimbus.signals