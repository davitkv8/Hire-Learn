from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=55, unique=True, null=True)

    ## !!! ## override this part, not members needed, insted of this use onetoone field to Relationship model.
    members = models.ManyToManyField(User, blank=False)

    def __repr__(self):
        return f"{self.chatroom} | {set(self.members.all().values_list('username', flat=True))}"
