import json

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime, time, date

from .forms import TeacherRegisterForm, TeacherProfileForm, StudentProfileForm
from .namings import STUDENT_PROFILE_FIELD_IDS_IN_FRONT,\
    TEACHER_FIELD_IDS_IN_FRONT, M2M_FIELDS, FOREIGN_KEY_FIELDS
from users.models import UserStatus, TeacherProfile, Image, StudentProfile, HashTag
from .helpers import parse_values_from_lists_when_ajax_resp,\
    validate_image, create_foreign_keys_where_necessary,\
    get_request_user_profile_model_and_fields


def get_user_profile_data(user):
    data = get_request_user_profile_model_and_fields(user)

    user_profile_obj = data['profile_obj']
    fields = data['front_fields']

    field_info_with_value = []

    for field in fields:

        try:
            value = getattr(user_profile_obj, field)

        except AttributeError:
            value = getattr(user, field)

        if field in M2M_FIELDS:
            value = [i for i in value.values_list(field, flat=True)]

        if field in FOREIGN_KEY_FIELDS:
            value = getattr(value, field)

        if field == "image":
            value = getattr(value, field).url

        if type(value) in [datetime, date, time]:
            value = value.strftime("%Y-%m-%d")

        fields[field]['value'] = value
        field_info_with_value.append({field: fields[field]})

    return json.dumps(field_info_with_value)


def user_profile_view(request, user_pk):

    context = {

    }

    if request.method == "GET":
        user = User.objects.get(pk=user_pk)
        # user_profile_model = get_request_user_profile_model(user)
        context['fields_data'] = get_user_profile_data(user)

    return render(request, "users/profile.html", context=context)


# class UpdateTeacherProfileView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
#     template_name = 'users/profile.html'
#     # context_object_name = 'object'
#
#     def dispatch(self, request, *args, **kwargs):
#         self._specify_fields_data_for_front()
#
#         return super(UpdateTeacherProfileView, self).dispatch(
#             request, *args, **kwargs)
#
#     def get_queryset(self):
#         pk = self.kwargs.get(self.pk_url_kwarg)
#
#         queryset = self._user_profile_model().objects.filter(
#             user_id=pk
#         )
#
#         self.kwargs.update(
#             {self.pk_url_kwarg: queryset.first().pk}
#         )
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['fields_data'] = get_user_profile_data(self.object)
#
#         # context['friendRequest'] = Relationship.objects.filter(receiver=self.object, status='send').all()
#         # context['hasTimeTable'] = TimeTable.objects.filter(user=self.object.user).first()
#         # context['feedbacks'] = self.object.feedback.all().order_by('date')[:10]
#         # context['verification_request'] = email_verification(request=self.request, pk=self.request.user.pk)
#         return context
#
#     def test_func(self):
#         return self.request.user
#
#     def form_valid(self, form):
#         # form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def get(self, request, *args, **kwargs):
#
#         return super().get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         # if request.is_ajax():
#         #     if request.POST["type"] == "verify_request":
#         #         email_verification(self.request, request.POST["user"])
#         #         return HttpResponse()
#         #
#         #     rel = Relationship.objects.get(receiver=request.user.teachersprofile,
#         #                                    sender=request.POST["user"], status="send")
#         #     if request.POST["type"] == "approve":
#         #         rel.status = "Approve"
#         #         rel.save()
#         #     else:
#         #         rel.delete()
#         #
#         #     return HttpResponse()
#         # else:
#         return super().post(request, *args, **kwargs)
#
#     def _user_profile_model(self):
#         return get_request_user_profile_model(self.request)
#
#     def _specify_fields_data_for_front(self):
#         fields_info = self._user_profile_model().specific_fields_for_front()
#         fields_info = {
#             key: value for key, value in fields_info.items()
#             if not fields_info[key].get('non_related_class')
#            }
#
#         self.fields = [
#             field for field in fields_info
#             if fields_info[field]['editable']
#         ]
#
#         self.readonly_fields = [
#             field for field in fields_info
#             if not fields_info[field]['editable']
#         ]
#
#     def get_success_url(self):
#         return reverse('teacher-profile', kwargs={'pk': self.object.pk})


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

