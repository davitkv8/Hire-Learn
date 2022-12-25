from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import UserProfile, Platform


class UserRegisterForm(UserCreationForm):
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


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['birth_date', 'full_name', 'lecture_price',
                  'description', 'platform', 'title']
        widgets = {
            'birth_date': forms.DateInput(attrs={'required': 'required', 'type': 'date'}),
            'description': forms.Textarea(attrs={"style": "resize: none"})
        }

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', '')
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['platform'] = forms.ModelChoiceField(
            queryset=Platform.objects.all().values_list('platform', flat=True)
        )

