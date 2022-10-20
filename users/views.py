from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import FileSystemStorage

from .forms import TeacherRegisterForm, TeacherProfileForm, UserProfileForm

from users.models import UserStatus, TeachersProfile


class Login(LoginView):
    template_name = 'users/login.html'


def register(request):
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

            # if request.POST['user'] == 'teacher':
            #     registered_user.save()
            return redirect('complete-user', registered_user.pk)
            #
            # elif request.POST['user'] == 'student':
            #     registered_user.save()
            #     return redirect('main-view')

    return render(request, 'users/register.html', {'form': form})


@login_required
def complete_user_registration(request, pk):  # User's Primary key

    if request.user.pk != pk:
        return redirect('main-view')

    user_status = UserStatus.objects.get(user=request.user).userStatus

    if user_status == 'student':
        form = {user_status: UserProfileForm}

    else:
        form = {user_status: TeacherProfileForm}

    if request.method == 'POST':
        form = form[user_status](request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            teacher_profile_object = TeachersProfile(birth_date=form_data['birth_date'],
                                                     full_name=form_data['full_name'],
                                                     lecture_price=form_data['lecture_price'],
                                                     description=form_data['description'],
                                                     platform=form_data['platform'],
                                                     subject=form_data['subject'],
                                                     image=request.FILES['image'], user=request.user)
            teacher_profile_object.save()
            # return email_verification(request, pk)

    user_full_name = request.user.first_name + ' ' + request.user.last_name

    return render(request, 'users/complete_user.html', {'form': form, 'full_name': user_full_name})


@csrf_exempt
@login_required
def ajax_file_upload_save(request):
    file1 = request.FILES['file1']
    fs = FileSystemStorage()
    file_1_path = fs.save(file1.name, file1)
    print(file_1_path)
    return HttpResponse("Uploaded")

