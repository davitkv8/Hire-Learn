from users.forms import StudentProfileForm, TeacherProfileForm

VISIBLE_FIELDS_IN_STUDENTS_PROFILE_PAGE = {

    "description": {
        "name_in_front": "Description",
        "editable": True,
    },

    "hashtags": {
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

STUDENT_PROFILE_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in StudentProfileForm.Meta.fields
}


TEACHER_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in TeacherProfileForm.Meta.fields
}
