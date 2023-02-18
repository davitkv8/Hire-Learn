from django.urls import path, re_path
from chatroom.views import *

urlpatterns = [
    path('inbox/', chatroom, name='chat_room_default_page'),
]
