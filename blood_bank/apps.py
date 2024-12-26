from django.apps import AppConfig

class BloodBankConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blood_bank"

    def ready(self):
        import blood_bank.signals  # Import the signals to connect them to the user model


