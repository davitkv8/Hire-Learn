from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from classroom.models import Relationship
from chatroom.models import ChatRoom
import secrets
import string


@receiver(post_save, sender=Relationship)
def create_chat_room(sender, instance, created, **kwargs):
    # On relationship approves, it will automatically create new chat room for users.
    if instance.is_confirmed:
        default_chatroom = ''.join(
            secrets.choice(string.ascii_uppercase + string.ascii_lowercase)
            for i in range(55)
        )
        created = ChatRoom.objects.create(chatroom=default_chatroom)
        created.members.set([instance.sender, instance.receiver])
