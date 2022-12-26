import json

from django.shortcuts import render, redirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

from .forms import TeacherRegisterForm, TeacherProfileForm, StudentProfileForm

from .namings import STUDENT_PROFILE_FIELD_IDS_IN_FRONT,\
    TEACHER_FIELD_IDS_IN_FRONT, M2M_FIELDS, FOREIGN_KEY_FIELDS

from users.models import UserStatus, TeacherProfile, Image, StudentProfile, HashTag

from .helpers import parse_values_from_lists_when_ajax_resp,\
    validate_image, create_foreign_keys_where_necessary,\
    get_request_user_profile_model_and_fields,\
    get_user_profile_data

from classroom.services import get_booking_requests
from classroom.models import *

@login_required
def get_names(request):
    field = request.GET.get('field').split("-")[0]
    search = request.GET.get('search')

    field_class = FOREIGN_KEY_FIELDS[field]
    query_str = f"{field}__startswith"

    payload = []

    if search:
        objs = field_class.objects.filter(
            **{query_str: search}
        )
        for obj in objs:
            payload.append(
                {'name': obj.platform}
            )
    print(payload)
    return HttpResponse(
        json.dumps({
            'status': True,
            'payload': payload,
        })
    )


@login_required
def user_profile_view(request, user_pk=None):

    context = {

    }

    requested_user = User.objects.get(pk=user_pk)  # User who's profile is requested to see
    request_user = request.user  # Just request user.

    if request.method == "GET":
        context['fields_data'] = get_user_profile_data(requested_user)
        context['requested_user'] = requested_user

        context['bookingRequests'] = get_booking_requests(
            **{"receiver_id": requested_user.id, "is_confirmed": False}
        )

        context["feedbacks"] = Feedback.objects.filter(
            receiver=request.user
        )

        return render(request, "users/profile.html", context=context)

    if request.method == "POST":
        try:

            if request_user == requested_user:
                data = parse_values_from_lists_when_ajax_resp(dict(request.POST))
                profile_model = get_request_user_profile_model_and_fields(requested_user)['model_class']
                data = create_foreign_keys_where_necessary(profile_model, data)

                profile_model.objects.filter(user=requested_user).update(
                    **data
                )

                return HttpResponse(
                    json.dumps({
                        "status": 200,
                        "message": "Successfully updated"
                    })
                )

            return HttpResponse(
                json.dumps({
                    "status": 404,
                    "message": "Invalid Request"
                })
            )

        except Exception as e:
            print(e)
            return HttpResponse(
                json.dumps({
                    "status": 204,
                    "message": "Please, fill in correct data"
                })
            )


class Login(LoginView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main-view")
        return super().get(request)


def register(request):
    if request.user.is_authenticated:
        return redirect("main-view")

    form = TeacherRegisterForm
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            user_data = form.cleaned_data

            registered_user = User.objects.get(username=user_data['username'])

            UserStatus.objects.create(user=registered_user, userStatus=request.POST['userStatus'])

            new_user = authenticate(username=user_data['username'],
                                    password=user_data['password1'],
                                    )

            login(request, new_user)
            return redirect('complete-user', registered_user.pk)

    return render(request, 'users/register.html', {'form': form})


def get_registration_field_namings(request):
    if request.user.userstatus.userStatus == 'student':
        helpers = STUDENT_PROFILE_FIELD_IDS_IN_FRONT
    else:
        helpers = TEACHER_FIELD_IDS_IN_FRONT

    return HttpResponse(json.dumps(helpers))


@login_required
def hash_tags(request):

    if request.method == "POST":

        key = "hashTag"
        request_data = request.POST
        data = request_data.getlist(key + "[]")
        items = [HashTag(hashTag=hash_tag) for hash_tag in data]

        try:

            HashTag.objects.bulk_update_or_create(
                items, [key], match_field="hashTag"
            )

            committed_and_saved_data = list(
                HashTag.objects.filter(hashTag__in=data)
            )

            request.user.basicabstractprofile.hashTag.add(
                *committed_and_saved_data
            )

            url = reverse("main-view")
            return JsonResponse(status=200, data={'success': url})

        except Exception as e:
            print(e)

    return render(request, 'users/hashTags.html')


# @csrf_exempt
@login_required
def complete_user_registration(request, pk):  # User's Primary key

    if request.user.pk != pk:
        return redirect('main-view')

    user_status = UserStatus.objects.get(user=request.user).userStatus

    if user_status == 'student':
        form = StudentProfileForm

    else:
        form = TeacherProfileForm

    if request.method == 'POST':

        data = parse_values_from_lists_when_ajax_resp(dict(request.POST))
        data['user'] = request.user

        if validate_image(request.FILES['file1']):
            image_obj = Image.objects.create(image=request.FILES['file1'])
            data['image'] = image_obj

        data = create_foreign_keys_where_necessary(form.Meta.model, data)

        form.Meta.model.objects.create(**data)

        url = reverse('hashTag')

        return JsonResponse(status=302, data={'success': url})

    user_full_name = request.user.first_name + ' ' + request.user.last_name
    # return redirect("register")
    return render(request, 'users/complete_user.html',
                  {'form': form, 'full_name': user_full_name})


@login_required
def string_matcher(request):

    user_input = request.GET['inputData']
    suggestions = list(
        HashTag.objects.filter(
            hashTag__icontains=user_input).values_list("hashTag", flat=True)
    )

    return HttpResponse(
        json.dumps(
            {
                "suggestions": suggestions
            }
        )
    )
