from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from chatroom.models import MessageRoom, CurrentlyActiveWSChannels
from asgiref.sync import async_to_sync
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name =self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = await database_sync_to_async(self.currently_active_wss)()


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        print("DISCONNECTING!!!!")
        await database_sync_to_async(self.delete_active_wss)()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_py = json.loads(text_data)

        message = text_data_py['message']
        sender = text_data_py['sender']
        receiver = text_data_py['receiver']
        await database_sync_to_async(self.send_message_to_db)(message, sender, receiver)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
            }
        )

    def send_message_to_db(self, message=None, sender=None, receiver=None):
        return MessageRoom.objects.create(
            sender=User.objects.get(username=sender),
            receiver=User.objects.get(username=receiver),
            message=message,
        )

    def currently_active_wss(self):
        _, obj = CurrentlyActiveWSChannels.objects.get_or_create(
            group_name=self.room_name
        )
        return _.group_name

    def delete_active_wss(self):
        return CurrentlyActiveWSChannels.objects.filter(
            group_name=self.room_group_name
        ).delete()

    async def chatroom_message(self, event):
        message = event['message']
        username = event['receiver']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
