"""
    THOSE FUNCTIONS ARE ADDED AS HELPER FUNCTIONS FOR CERTAIN CASES
"""
import imghdr
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ForeignKey
from django.shortcuts import redirect
from django.urls import reverse

from users.models import StudentProfile, TeacherProfile
from users.namings import (
            VISIBLE_FIELDS_IN_STUDENTS_PROFILE_PAGE,
            VISIBLE_FIELDS_IN_TEACHERS_PROFILE_PAGE
        )

FIELDS_TO_BE_IGNORED = [
    'user_status',
]


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
    return {
        key.replace("[]", ""): value[0]
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

        if type(field) == ForeignKey:

            instance, created = field.remote_field.model.objects.get_or_create(
                **{field_name: data[field_name]},
                defaults={field_name: data[field_name]}
            )

            data[field_name] = instance

    return data
