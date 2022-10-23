import json

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse

from .forms import TeacherRegisterForm, TeacherProfileForm, UserProfileForm
from .namings import USERPROFILE_FIELD_IDS_IN_FRONT, TEACHER_FIELD_IDS_IN_FRONT
from users.models import UserStatus, TeachersProfile, Image, UserProfile, HashTag
from .helpers import parse_values_from_lists_when_ajax_resp, validate_image


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
        helpers = USERPROFILE_FIELD_IDS_IN_FRONT
    else:
        helpers = TEACHER_FIELD_IDS_IN_FRONT

    return HttpResponse(json.dumps(helpers))


def hash_tags(request):

    if request.method == "POST":

        key = "hashTag"
        data = request.POST.getlist(key + "[]")
        items = [HashTag(hashTag=hash_tag) for hash_tag in data]

        try:

            HashTag.objects.bulk_update_or_create(
                items, [key], match_field="hashTag"
            )

            committed_and_saved_data = list(
                HashTag.objects.filter(hashTag__in=data)
            )

            request.user.userprofile.hashtags.add(
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
        form = UserProfileForm

    else:
        form = TeacherProfileForm

    if request.method == 'POST':

        data = parse_values_from_lists_when_ajax_resp(dict(request.POST))
        data['user'] = request.user

        if validate_image(request.FILES['file1']):
            image_obj = Image.objects.create(image=request.FILES['file1'])
            data['image'] = image_obj

        form.Meta.model.objects.create(**data)

        url = reverse('hashTags')

        return JsonResponse(status=302, data={'success': url})

    user_full_name = request.user.first_name + ' ' + request.user.last_name
    # return redirect("register")
    return render(request, 'users/complete_user.html',
                  {'form': form, 'full_name': user_full_name})


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

