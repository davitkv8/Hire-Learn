from users.namings import VISIBLE_FIELDS_IN_USERS_PROFILE_PAGE

TEACHER_CARD_FIELDS = (
    "full_name", "image", "title"
)

TEACHER_CARD_FIELDS_DATA = {
    key: value for key, value in VISIBLE_FIELDS_IN_USERS_PROFILE_PAGE.items()
    if key in TEACHER_CARD_FIELDS
}
