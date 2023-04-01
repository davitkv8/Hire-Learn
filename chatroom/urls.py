from django.urls import path, re_path
from chatroom.views import *

urlpatterns = [
    path('inbox/', inbox, name='chat_room_default_page'),
    path('inbox/change_room/', chat_room, name='chat_room')
]
