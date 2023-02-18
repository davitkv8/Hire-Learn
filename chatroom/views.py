from django.shortcuts import render


def chatroom(request):
    return render(request, 'chatroom/index.html',
                  {'room_name': "room_name", 'messages': "messages",
                   'chattingWith': "chattingwith", 'totalMessages': 50,
                   'chatMembers': "relationships", 'is_seen': "is_seen",
                   "is_teacher": "get_user_status()"
                   }
                  )
