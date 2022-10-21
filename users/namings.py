from users.forms import UserProfileForm, TeacherProfileForm

USERPROFILE_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in UserProfileForm.Meta.fields
}


TEACHER_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in TeacherProfileForm.Meta.fields
}
