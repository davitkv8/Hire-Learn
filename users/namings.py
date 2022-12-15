from users.forms import StudentProfileForm, TeacherProfileForm
from django.contrib.auth.models import User
from users.models import *

VISIBLE_FIELDS_IN_STUDENTS_PROFILE_PAGE = {
    "username": {
        "name_in_front": "Username",
        "editable": True,
        "field_type": "string",
    },

    "description": {
        "name_in_front": "Description",
        "editable": True,
        "field_type": "string",
    },

    "hashTag": {
        "name_in_front": "Tags",
        "editable": False,
        "field_type": "selection+",
    },

    "image": {
        "name_in_front": "Profile Picture",
        "editable": True,
        "field_type": "string",
    },

    "record_creation_datetime": {
        "name_in_front": "Since",
        "editable": False,
        "field_type": "datetime",
    }
}


VISIBLE_FIELDS_IN_TEACHERS_PROFILE_PAGE = {

    "full_name": {
        "name_in_front": "Full Name",
        "editable": True,
        "field_type": "string",
    },

    "email": {
        "name_in_front": "E-mail",
        "editable": False,
        "field_type": "string",
    },

    "birth_date": {
        "name_in_front": "Birth Date",
        "editable": True,
        "field_type": "date",
    },

    "title": {
        "name_in_front": "Title",
        "editable": True,
        "field_type": "string",
    },

    "lecture_price": {
        "name_in_front": "Lecture Price (Per hour)",
        "editable": True,
        "field_type": "int",
    },

    "platform": {
        "name_in_front": "Platform",
        "editable": True,
        "field_type": "selection",
    },

    "hashTag": {
        "name_in_front": "Tags",
        "editable": False,
        "field_type": "selection+",
    },

    "image": {
        "name_in_front": "Profile Picture",
        "editable": False,
        "field_type": "string",
    },

    "record_creation_datetime": {
        "name_in_front": "Since",
        "editable": False,
        "field_type": "datetime",
    },

    "description": {
        "name_in_front": "Description",
        "editable": True,
        "field_type": "string",
    },

    "timeGraph": {
        "name_in_front": "You have not set time graph yet."
                         "please, set it to be visible for other users.",
        "editable": False,
        "field_type": "alert alert-danger",
    }

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
    "platform": Platform,
    "timeGraph": TimeGraph,
}

M2M_FIELDS = {
    "hashTag": HashTag,
    "friends": User,
}

