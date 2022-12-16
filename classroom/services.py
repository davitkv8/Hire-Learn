from classroom.models import *


def send_or_approve_booking_request(
        sender_id: "User PK", receiver_id: "User PK",
        agreed_days: dict, is_confirmed: bool = False,
):
    Relationship.objects.get_or_create(
        sender_id=sender_id, receiver_id=receiver_id,
        defaults={
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "agreed_days": agreed_days,
            "is_confirmed": is_confirmed,
        }
    )


def get_booking_requests(**kwargs):
    return Relationship.objects.filter(**kwargs)
