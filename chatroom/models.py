from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=55, unique=True, null=True)
    members = models.ManyToManyField(User, blank=False)

    def __repr__(self):
        return f"{self.chatroom} | {self.members}"
