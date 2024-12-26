# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from admin_notifications.models import Notification

@receiver(post_save, sender=User)
def create_welcome_notification(sender, instance, created, **kwargs):
    if created:  # Only when a new user is created
        Notification.objects.create(
            recipient=instance,
            title="Welcome!",
            message=f"Welcome to our platform, {instance.username}!",
            notification_type="success"
        )
        
        
