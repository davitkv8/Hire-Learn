"""
    THOSE FUNCTIONS ARE ADDED AS HELPER FUNCTIONS FOR CERTAIN CASES
"""
import imghdr
from django.shortcuts import redirect
from django.urls import reverse


def parse_values_from_lists_when_ajax_resp(obj):
    return {
        key.replace("[]", ""): value[0]
        for key, value in obj.items() if key != 'csrfmiddlewaretoken'
    }


def validate_image(file):
    if imghdr.what(file):
        return True
    return False

