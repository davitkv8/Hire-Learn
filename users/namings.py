from users.forms import StudentProfileForm, TeacherProfileForm
from django.contrib.auth.models import User
from users.models import *

VISIBLE_FIELDS_IN_STUDENTS_PROFILE_PAGE = {
    "username": {
        "name_in_front": "Username",
        "editable": True,
    },

    "description": {
        "name_in_front": "Description",
        "editable": True,
    },

    "hashTag": {
        "name_in_front": "Tags",
        "editable": True,
    },

    "image": {
        "name_in_front": "Profile Picture",
        "editable": True,
    },

    "record_creation_datetime": {
        "name_in_front": "Since",
        "editable": False,
    }
}


VISIBLE_FIELDS_IN_TEACHERS_PROFILE_PAGE = {

    "description": {
        "name_in_front": "Description",
        "editable": True,
    },

    "hashTag": {
        "name_in_front": "Tags",
        "editable": True,
    },

    "image": {
        "name_in_front": "Profile Picture",
        "editable": True,
    },

    "record_creation_datetime": {
        "name_in_front": "Since",
        "editable": False,
    },

    "birth_date": {
        "name_in_front": "birth_date",
        "editable": False,
    },

    "full_name": {
        "name_in_front": "full_name",
        "editable": False,
    },

    "lecture_price": {
        "name_in_front": "lecture_price",
        "editable": False,
    },

    "platform": {
        "name_in_front": "platform",
        "editable": False,
    },

    "subject": {
        "name_in_front": "subject",
        "editable": False,
    },

}


STUDENT_PROFILE_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in StudentProfileForm.Meta.fields
}


TEACHER_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in TeacherProfileForm.Meta.fields
}


FOREIGN_KEY_FIELDS = {
    "user_status": UserStatus,
    "subject": Subject,
}

M2M_FIELDS = {
    "hashTag": HashTag,
    "friends": User
}

