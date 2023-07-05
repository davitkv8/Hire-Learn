from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users.helpers import get_request_user_profile_model_and_fields, create_foreign_keys_where_necessary
from users.models import TeacherProfile, StudentProfile
from classroom.services import create_booking_request, get_booking_requests
from classroom.namings import TEACHER_CARD_FIELDS_DATA
from classroom.services import default_json_serializer
from classroom.models import *
from users.helpers import parse_values_from_lists_when_ajax_resp, get_user_profile_data
from django.db.models import Q

import copy
import json


TEMPLATE_DAYS_DATA = json.load(
    open('template_days_data.json')
)

@login_required
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
        ).first()

        # Do not use update here, while we need to catch it for signals
        rel_obj.is_confirmed = data['is_confirmed']
        rel_obj.save()

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


def get_pivottable_data(*args):

    rel_query, feedback_query = args

    feedback_data = {
        dict_data['sender__username']: dict_data['rating']
        for dict_data in feedback_query
    }

    pivottable_data = []

    for data_dict in rel_query:
        pivot_object = {}

        for key, value in data_dict.items():
            new_key = key.split("__")[-1]
            pivot_object[new_key] = data_dict[key]

            # Calculate agreed hours in the week
            if new_key == "agreed_days":
                pivot_object['Total Days'] = 0

                for agreed_day in list(pivot_object[new_key].values()):
                    pivot_object['Total Days'] += len(agreed_day)

                pivot_object['Profit Wage'] = pivot_object['Total Days'] * 12.5

                pivot_object['Profit After Tax'] = \
                    pivot_object['Profit Wage'] - (pivot_object['Profit Wage'] * 5 / 100)

        pivot_object['rating'] = feedback_data.get(
            pivot_object['username']
        )

        pivottable_data.append(pivot_object)

    return pivottable_data


@login_required
def classroom(request):
    model_class = get_request_user_profile_model_and_fields(request.user)['model_class']

    # TEACHERS AND STUDENTS SHOULD HAVE DIFFERENT VERS OF CLASSROOM
    # MAYBE IT WOULD BE NICER TO USE THIS FUNCTION AS REDIRECT ONE
    # WHICH CALL APPROPRIATE VIEW DEPENDING ON USER PROFILE MODEL
    # BUT FOR NOW LEAVE IT AS IT IS

    if model_class is TeacherProfile:

        rel_query = Relationship.objects.filter(receiver=request.user)\
            .values(
            "sender__username", "agreed_days",
            "record_creation_datetime__date", "is_confirmed",
        )

        feedbacks_query = Feedback.objects.filter(
            sender__username__in=rel_query.values_list("sender__username", flat=True),
            receiver=request.user
        ).values("sender__username", "rating")

        data = get_pivottable_data(rel_query, feedbacks_query)

        return render(
            request,
            "classroom/stats_pivottable.html",
            {
                "json_data": json.dumps(data, default=default_json_serializer),
            },
        )

    elif model_class is StudentProfile:

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

    else:
        return HttpResponse(status=404)
