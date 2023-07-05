from classroom.models import *
from datetime import datetime, date, time, timedelta
import pandas as pd


def create_booking_request(
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


def default_json_serializer(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
