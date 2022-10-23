from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import TeacherProfile, StudentProfile


class TeacherRegisterForm(UserCreationForm):
    email = models.EmailField(unique=True, null=False, blank=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'required': 'required'})
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")


class TeacherProfileForm(forms.ModelForm):

    class Meta:
        model = TeacherProfile
        fields = ['birth_date', 'full_name', 'lecture_price',
                  'description', 'platform', 'subject']
        widgets = {
            'birth_date': forms.DateInput(attrs={'required': 'required', 'type': 'date'}),
            'description': forms.Textarea(attrs={"style": "resize: none"})
        }


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ['description']
        widgets = {
            # 'birth_date': forms.DateInput(attrs={'required': 'required', 'type': 'date'}),
            'description': forms.Textarea(attrs={"style": "resize: none"})
        }

