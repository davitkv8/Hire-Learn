from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Relationship, TeacherProfile
from classroom.models import TimeGraph
import json


class AjaxTimeTable(View):

    def get(self, request, user_pk):
        user_table = TimeGraph.objects.filter(user=user_pk).first()
        if user_table is None:
            return render(request, 'classroom/time_table.html', {"object": int(user_pk)})
        return render(request, 'classroom/time_table.html', {'days': user_table.available_time,
                                                             "object": int(user_pk)})

    def post(self, request, user_pk):
        user_pk = int(user_pk)
        user = User.objects.get(pk=user_pk)
        days = request.POST['availableDays']
        days = json.loads(days)
        created = TimeGraph.objects.filter(user=request.user).first()

        if request.user == user:
            if created is None:
                created = TimeGraph.objects.create(user=request.user)
                created.available_time = []
            for day in days['availableDays']:
                created.available_time.append(day)

            for day in days['unavailableDays']:
                if day in created.available_time:
                    created.available_time.remove(day)

            created.save()

        else:
            relationship = Relationship.objects.create(sender=request.user,
                                                       receiver=TeacherProfile.objects.get(pk=user.teachersprofile.pk),
                                                       status="send")
            relationship.available_time = []
            for day in days['availableDays']:
                relationship.available_time.append(day)
            relationship.save()
        return HttpResponse()
