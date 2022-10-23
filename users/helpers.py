"""
    THOSE FUNCTIONS ARE ADDED AS HELPER FUNCTIONS FOR CERTAIN CASES
"""
import imghdr
from django.db.models.fields.related import ForeignKey
from django.shortcuts import redirect
from django.urls import reverse


def parse_values_from_lists_when_ajax_resp(obj):
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

        if type(field) == ForeignKey:

            field_name = field.name
            instance, created = field.remote_field.model.objects.get_or_create(
                **{field_name: data[field_name]},
                defaults={field_name: data[field_name]}
            )

            data[field_name] = instance

    return data
