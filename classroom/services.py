from classroom.models import *
from datetime import datetime, date, time, timedelta
import pandas as pd

WEEK_DAYS = (
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday"
)


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


def get_nearest_lesson(*args):
    """
        This script returns nearst lesson from iterable,
        for example, if user lessons iterable object is -> {'sunday': ['3:00-4:00'], 'tuesday': ['3:00-4:00']}
        and today is friday, then nearest lesson will be 'sunday': ['3:00-4:00']
    :param args:
    :return:
    """

    if not args:
        return None

    week_day_index = datetime.today().weekday()
    user_lessons_graph_dict, = args

    days_remaining_to_next_lesson = 0

    while True:
        try:
            week_day = WEEK_DAYS[week_day_index]
            if week_day in user_lessons_graph_dict:
                today = datetime.today()

                lesson_time = user_lessons_graph_dict[week_day][0].split(":")

                lesson_datetime = today + timedelta(days=days_remaining_to_next_lesson)
                lesson_datetime = lesson_datetime.replace(
                    hour=int(lesson_time[0]), minute=int(lesson_time[-1])
                )

                return lesson_datetime

            week_day_index += 1

        except IndexError:
            week_day_index = 0

        finally:
            if days_remaining_to_next_lesson >= 7:
                return None

            days_remaining_to_next_lesson += 1
