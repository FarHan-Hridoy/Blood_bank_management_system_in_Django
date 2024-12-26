
from django.apps import AppConfig

class AdminNotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_notifications'

    def ready(self):
        import admin_notifications.signals