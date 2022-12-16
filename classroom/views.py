from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Relationship, TeacherProfile
from classroom.models import TimeGraph
from users.helpers import get_request_user_profile_model_and_fields, create_foreign_keys_where_necessary
import copy
import json


TEMPLATE_DAYS_DATA = json.load(
    open('template_days_data.json')
)


class AjaxTimeTable(View):

    def get(self, request, user_pk):

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

    def post(self, request, user_pk):

        template_data = copy.deepcopy(TEMPLATE_DAYS_DATA)
        time_graph_data = json.loads(request.POST['days_data'])

        # incoming data -> {monday: [{'0:00-1:00': 'false'}, {'1:00-2:00': 'false'}, ...]}
        # dict where values are list of dictionaries
        # edited data ->  {'wednesday': {'0:00-1:00': 'false', '10:00-11:00': 'false', ...}
        # just parsing values and storing them as dict itself.

        for key, list_value in time_graph_data.items():
            for key_value in list_value:
                template_data[key][key_value] = True

        request_user_id = request.user.id
        requested_user_id = int(user_pk)

        # student sending request to teacher case
        if request_user_id != requested_user_id:
            pass

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


        #
        # else:
        #     relationship = Relationship.objects.create(sender=request.user,
        #                                                receiver=TeacherProfile.objects.get(pk=user.teachersprofile.pk),
        #                                                status="send")
        #     relationship.available_time = []
        #     for day in days['availableDays']:
        #         relationship.available_time.append(day)
        #     relationship.save()
        # return HttpResponse()
