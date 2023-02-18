from django.shortcuts import render
from classroom.models import Relationship
from django.db.models import Q


def chatroom(request):

    relationships = Relationship.objects.filter(
        Q(receiver=request.user) | Q(sender=request.user)
    ).values_list()

    return render(request, 'chatroom/index.html',
                  {'room_name': "room_name", 'messages': "messages",
                   'chattingWith': "chattingwith", 'totalMessages': 50,
                   'chatMembers': "relationships", 'is_seen': "is_seen",
                   "is_teacher": "get_user_status()"
                   }
                  )
