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
        "editable": False,
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

    "full_name": {
        "name_in_front": "Full Name",
        "editable": True,
    },

    "email": {
        "name_in_front": "E-mail",
        "editable": False,
    },

    "birth_date": {
        "name_in_front": "Birth Date",
        "editable": True,
    },

    "title": {
        "name_in_front": "Title",
        "editable": True,
    },

    "lecture_price": {
        "name_in_front": "Lecture Price (Per hour)",
        "editable": True,
    },

    "platform": {
        "name_in_front": "Platform",
        "editable": True,
    },

    "hashTag": {
        "name_in_front": "Tags",
        "editable": False,
    },

    "image": {
        "name_in_front": "Profile Picture",
        "editable": False,
    },

    "record_creation_datetime": {
        "name_in_front": "Since",
        "editable": False,
    },

    "description": {
        "name_in_front": "Description",
        "editable": True,
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
    "title": Title,
}

M2M_FIELDS = {
    "hashTag": HashTag,
    "friends": User
}

