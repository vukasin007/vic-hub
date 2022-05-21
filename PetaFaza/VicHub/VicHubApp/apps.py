from django.apps import AppConfig
# vukasin007


class VichubappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'VicHubApp'

    # ---------- for celery ------------
    def ready(self):
        # Import celery app now that Django is mostly ready.
        # This initializes Celery and autodiscovers tasks
        import VicHub.celery
    # ----------------------------------
