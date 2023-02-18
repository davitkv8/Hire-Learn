from django.urls import re_path
from chatroom.consumers import ChatRoomConsumer

websocket_urlpatterns = [
    re_path(r"chat/(?P<room_name>\w+)/$", ChatRoomConsumer.as_asgi())
]
