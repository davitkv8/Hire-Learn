from django.shortcuts import render
from classroom.models import Relationship
from chatroom.models import MessageRoom, CurrentlyActiveWSChannels
from django.db.models import Q
from django.http import JsonResponse
from users.helpers import get_user_based_query_str, parse_values_from_lists_when_ajax_resp
from chatroom.namings import INBOX_MENU_LEFT_HAND_FIELD_VARIATIONS
from django.contrib.auth.models import User

from urllib.parse import urlparse


def get_avail_chat_users(request):

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

    return rel_data


def chat_room(request):
    response_data = {

    }

    url = request.build_absolute_uri()
    parsed_url = urlparse(url)

    running_host_address = f"{parsed_url.hostname}:{parsed_url.port}"

    request_data = parse_values_from_lists_when_ajax_resp(dict(request.GET))
    response_data['chatting_with'] = request_data['chat_member']
    chat_member_user_obj = User.objects.get(
       **{'username': response_data['chatting_with']}
    )

    total_messages = MessageRoom.objects.filter(
        Q(
            sender__username=request.user.username,
            receiver__username=request_data['chat_member']
        ) |
        Q(
            sender__username=request_data['chat_member'],
            receiver__username=request.user.username,
        )
    ).order_by('create_datetime')

    response_data['messages_count'] = total_messages.count()

    response_data['messages'] = total_messages.values(
            'receiver__username', 'sender__username', 'create_datetime', 'message'
    )[:70]

    response_data['user_image'] = chat_member_user_obj.basicabstractprofile.image.image.url

    try:
        response_data['wss_url'] = CurrentlyActiveWSChannels.objects.get(
            Q(group_name=f"chat__{request.user.username}__{response_data['chatting_with']}") |
            Q(group_name=f"chat__{response_data['chatting_with']}__{request.user.username}")
        ).group_name

    except Exception as e:
        print(e)
        response_data['wss_url'] = f"chat__{request.user.username}__{response_data['chatting_with']}"

    connected_users = get_avail_chat_users(request)

    return render(
        request,
        'chatroom/index.html',
        context={
          "connected_users": connected_users,
          "details": response_data,
          "host": running_host_address
        }
    )


def inbox(request):

    connected_users = get_avail_chat_users(request)

    return render(
        request, 'chatroom/index.html',
        {"connected_users": connected_users}
    )
