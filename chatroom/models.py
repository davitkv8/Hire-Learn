from django.db import models
from django.contrib.auth.models import User
from classroom.models import Relationship
from django.utils import timezone
from cryptography.fernet import Fernet
import base64


class MessageRoom(models.Model):
    message = models.CharField(max_length=255, null=False, blank=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver')
    is_seen = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(default=timezone.now)
    seen_datetime = models.DateTimeField(null=True)

    def format_time(self):
        return self.create_datetime.strftime('%B %d, %H:%M')

    def __str__(self):
        return f'from {self.sender} to {self.receiver} on {self.create_datetime}'
