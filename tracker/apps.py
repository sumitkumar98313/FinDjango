from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        # import signals here so they get registered when the app starts
        # if we don't do this the signals won't work at all
        import tracker.signals
