from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"