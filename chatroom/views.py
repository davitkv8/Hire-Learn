from django.shortcuts import render
from classroom.models import Relationship
from django.db.models import Q
from users.helpers import get_user_based_query_str
from chatroom.namings import INBOX_MENU_LEFT_HAND_FIELD_VARIATIONS


def chat_room(request):
    pass


def inbox(request):

    req_user_type, opposite_user_type = get_user_based_query_str(request.user)

    _values = (opposite_user_type + i for i in INBOX_MENU_LEFT_HAND_FIELD_VARIATIONS)

    relationships = Relationship.objects.filter(
        **{
            req_user_type: request.user,
            'is_confirmed': True
        }
    ).values(*_values)

    rel_data = [

    ]

    for rel in relationships:
        rel_data.append({
            INBOX_MENU_LEFT_HAND_FIELD_VARIATIONS.get(key[key.find('_'):]): value
            for key, value in rel.items()
        })

    return render(request,
                  'chatroom/index.html',
                  {
                      "connected_users": rel_data
                  }
                  )




# {"messages": "messages",
#                    "chattingWith": "chattingwith", 'totalMessages': 50,
#                    "chatMembers": "relationships", 'is_seen': "is_seen",
#                    "is_teacher": "get_user_status()"
#                    }
#
#