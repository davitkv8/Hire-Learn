from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users.helpers import get_request_user_profile_model_and_fields, create_foreign_keys_where_necessary
from classroom.services import create_booking_request, get_booking_requests, get_nearest_lesson
from classroom.namings import TEACHER_CARD_FIELDS_DATA
from classroom.models import *
from users.helpers import parse_values_from_lists_when_ajax_resp, get_user_profile_data
from django.db.models import Q

import copy
import json


TEMPLATE_DAYS_DATA = json.load(
    open('template_days_data.json')
)


def send_booking_request(request):

    data = json.loads(request.POST['data'])

    requested_user_id, request_user_id, time_graph_data = data.values()

    try:
        # student sending request to teacher case
        if request_user_id != requested_user_id:
            create_booking_request(
                request_user_id, requested_user_id, time_graph_data
            )

        return HttpResponse(json.dumps({
            "status": 200,
            "message": "Your request has successfully sent to teacher\n"
                       "We will notify you on E-mail when teacher will give a response back to you.",
        }))

    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            "status": 404,
            "message": "There was error with your request",
        }))


class AjaxTimeTable(LoginRequiredMixin, View):

    def get(self, request, user_pk=None):
        template_data = copy.deepcopy(TEMPLATE_DAYS_DATA)

        if request.GET.get('booking_pk'):

            agreed_days = Relationship.objects.get(
                pk=int(request.GET.get('booking_pk'))
            ).agreed_days

            for key, list_value in agreed_days.items():
                for key_value in list_value:
                    template_data[key][key_value] = True

            context = {
                "days_data": template_data
            }

            return render(request, "classroom/time_table.html", context=context)

        request_user_id = request.user.id
        requested_user_id = int(user_pk)

        requested_user = User.objects.get(pk=requested_user_id)

        profile_model = get_request_user_profile_model_and_fields(requested_user)['model_class']
        profile = profile_model.objects.get(user=requested_user)

        time_graph = profile.timeGraph

        context = {
            "requested_user_id": requested_user_id,
            "request_user_id": request_user_id,
            "days_data": time_graph.timeGraph if time_graph else None
        }

        return render(request, 'classroom/time_table.html', context=context)

    def post(self, request):
        template_data = copy.deepcopy(TEMPLATE_DAYS_DATA)

        time_graph_data = json.loads(request.POST['days_data'])

        # incoming data -> {monday: [{'0:00-1:00': 'false'}, {'1:00-2:00': 'false'}, ...]}
        # dict where values are list of dictionaries
        # edited data ->  {'wednesday': {'0:00-1:00': 'false', '10:00-11:00': 'false', ...}
        # just parsing values and storing them as dict itself.

        for key, list_value in time_graph_data.items():
            for key_value in list_value:
                template_data[key][key_value] = True

        try:
            profile_model = get_request_user_profile_model_and_fields(request.user)['model_class']
            data = create_foreign_keys_where_necessary(
                profile_model,
                {"timeGraph": template_data}
            )

            profile_model.objects.filter(user=request.user).update(
                **data
            )

            return HttpResponse(json.dumps({
                "status": 200,
                "message": "Your Time Graph has saved successfully",
            }))

        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({
                "status": 404,
                "message": "Sorry, your request can't be handled",
            }))


@login_required
def response_booking(request):
    data = parse_values_from_lists_when_ajax_resp(dict(request.POST))

    try:
        rel_obj = get_booking_requests(
            receiver_id=data['receiver_id'],
            sender_id=data['sender_id']
        )

        rel_obj.update(**data)

        if data['is_confirmed']:
            rel = rel_obj.first()
            agreed_days = rel.agreed_days

            receiver_time_graph, sender_time_graph = [
                rel.receiver.basicabstractprofile.timeGraph,
                rel.sender.basicabstractprofile.timeGraph,
            ]

            for week_day, hours_list in agreed_days.items():
                for hour in hours_list:
                    receiver_time_graph.timeGraph[week_day][hour] = False
                    # sender_time_graph.timeGraph[week_day][hour] = rel.receiver

            receiver_time_graph.save()

        return HttpResponse(json.dumps(
            {
                "status": 200,
                "friends_count": get_booking_requests(
                 receiver_id=data['receiver_id'], is_confirmed=True
                ).count()
             }
        ))

    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({"status": 404}))


@login_required
def leave_feedback(request):
    data = parse_values_from_lists_when_ajax_resp(dict(request.POST))
    obj, created = Feedback.objects.get_or_create(
        receiver_id=data["receiver_id"],
        sender_id=data["sender_id"],

        defaults={
            **data,
        }
    )
    print(f"FEEDBACK CREATED {created}")
    if created:
        return HttpResponse(
            json.dumps({
                "status": 200,
                "message": "Thank you for sharing your experience!"
            })
        )

    return HttpResponse(
        json.dumps({
            "status": 404,
            "message": "You have already left feedback"
        })
    )


def classroom(request):
    rels = Relationship.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user),
            is_confirmed=True
        )

    cards_data = []

    for rel in rels:
        data = get_user_profile_data(
                rel.receiver, TEACHER_CARD_FIELDS_DATA, as_dict=True
            )

        data["next_lesson"] = get_nearest_lesson(rel.agreed_days)
        data["pk"] = rel.receiver_id
        cards_data.append(data)

    cards_data = sorted(cards_data, key=lambda x: x['next_lesson'])

    return render(request, 'classroom/classroom.html', {'cards_data': cards_data})
