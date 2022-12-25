from users.forms import UserProfileForm
from users.models import *

VISIBLE_FIELDS_IN_USERS_PROFILE_PAGE = {

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

    "get_relationship_counts": {
        "name_in_front": "Students",
        "editable": False,
        "field_type": "int",
    },

    "timeGraph": {
        "name_in_front": "You have not set time graph yet."
                         "please, set it to be visible for other users.",
        "editable": False,
        "field_type": "alert alert-danger",
    }

}


PROFILE_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in UserProfileForm.Meta.fields
}


FOREIGN_KEY_FIELDS = {
    "title": Title,
    "platform": Platform,
    "timeGraph": TimeGraph,
}

M2M_FIELDS = {
    "hashTag": HashTag,
    "friends": User,
}

