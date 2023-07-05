"""
    THOSE FUNCTIONS ARE ADDED AS HELPER FUNCTIONS FOR CERTAIN CASES
"""
import imghdr
import json

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# Verification imports
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .token_util import token_generator

from users.namings import (
            VISIBLE_FIELDS_IN_STUDENTS_PROFILE_PAGE,
            VISIBLE_FIELDS_IN_TEACHERS_PROFILE_PAGE,
            FOREIGN_KEY_FIELDS,
            M2M_FIELDS
        )

from users.producer import publish

from users.models import StudentProfile, TeacherProfile

from datetime import datetime, date, time
from copy import deepcopy

FIELDS_TO_BE_IGNORED = [
    'user_status',
]


def email_verification(request, pk):
    user = User.objects.filter(pk=pk).first()
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    link = reverse(
        'verification-view', kwargs={
            'uidb64': uidb64, 'token': token_generator.make_token(user)
        }
    )

    activate_url = 'http://' + domain + link
    email_subject = 'Account Verification'
    email_body = f"Hello {user.username} Please use this link to verify your account {activate_url}"

    data = {
        "subject": email_subject,
        "body": email_body,
        "sender": user.email
    }

    data = json.dumps(data)

    publish("message_alert", data)


def get_request_user_profile_model_and_fields(user):

    abstract_profile_class = user.basicabstractprofile

    # Just checking, if user has studentProfile or teacherProfile inheritance
    # And getting appropriate model class (not instance!)
    try:
        model_class = abstract_profile_class.studentprofile._meta.model
        front_fields = VISIBLE_FIELDS_IN_STUDENTS_PROFILE_PAGE

        profile_obj = getattr(
            user.basicabstractprofile,
            model_class.__name__.lower()
        )

        return {
            "model_class": model_class,
            "front_fields": front_fields,
            "profile_obj": profile_obj
        }

    except ObjectDoesNotExist:
        model_class = abstract_profile_class.teacherprofile._meta.model
        front_fields = VISIBLE_FIELDS_IN_TEACHERS_PROFILE_PAGE

        profile_obj = getattr(
            user.basicabstractprofile,
            model_class.__name__.lower()
        )

        return {
            "model_class": model_class,
            "front_fields": front_fields,
            "profile_obj": profile_obj
        }


def parse_values_from_lists_when_ajax_resp(obj: dict) -> dict:
    def convert_to_correct_dt(value):
        bool_variations = {
            "true": True,
            "false": False,
        }

        if value in bool_variations:
            return bool_variations[value]

        return value

    return {
        key.replace("[]", ""): convert_to_correct_dt(value[0])
        for key, value in obj.items() if key != 'csrfmiddlewaretoken'
    }


def validate_image(file):
    return imghdr.what(file) is not None


# This function is used to create foreign key data
def create_foreign_keys_where_necessary(model_class, data):
    # Looping over current Model class fields
    for field in model_class._meta.fields:

        field_name = field.name

        if field_name in FIELDS_TO_BE_IGNORED:
            continue

        if field_name in FOREIGN_KEY_FIELDS:
            try:
                instance, created = field.remote_field.model.objects.get_or_create(
                    **{field_name: data[field_name]},
                    defaults={field_name: data[field_name]}
                )

                data[field_name] = instance

            except KeyError:
                continue

    return data


def get_user_profile_data(user: User, only_certain_fields=None, as_dict=False):
    data = get_request_user_profile_model_and_fields(user)

    user_profile_obj = data['profile_obj']
    fields = only_certain_fields or data['front_fields']

    field_info_with_value = []

    for field in fields:

        try:
            value = getattr(user_profile_obj, field)

        except AttributeError:
            value = getattr(user, field)

        # If value is model method
        if callable(value):
            try:
                value = value()
            # ManyRelated comes with __call__ method
            except TypeError:
                pass

        # If value is foreign key instance, which is not created yet
        if value is None:
            fields[field]['value'] = value
            field_info_with_value.append({field: fields[field]})
            continue

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

    if as_dict:
        return deepcopy(fields)

    return json.dumps(field_info_with_value)


def get_user_based_query_str(user: User):
    """
        This function just gets user object and returns query str,
        as user should be receiver or sender.

        for example, if user is Teacher, she could be always receiver,
        as he is never send booking request to anyone else
    """

    sender_receiver = ['sender', 'receiver']

    model_class = get_request_user_profile_model_and_fields(user)['model_class']

    if model_class is TeacherProfile:
        sender_receiver.reverse()
        return sender_receiver

    elif model_class is StudentProfile:
        return sender_receiver

