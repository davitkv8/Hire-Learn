from users.forms import StudentProfileForm, TeacherProfileForm

STUDENT_PROFILE_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in StudentProfileForm.Meta.fields
}


TEACHER_FIELD_IDS_IN_FRONT = {
    field: "id_" + field for field in TeacherProfileForm.Meta.fields
}
