from django.db import models
from django.contrib.auth.models import User
from classroom.models import Relationship


class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=55, unique=True, null=True)
    # members = models.OneToOneField(Relationship, on_delete=models.SET_NULL)

    def get_members(self):
        self.members.objects.filter()
