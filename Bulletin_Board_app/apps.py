from django.apps import AppConfig


class BulletinBoardAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bulletin_Board_app'

    def ready(self):
        import Bulletin_Board_app.signals  # noqa