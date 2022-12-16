from django.urls import path, re_path
from classroom.views import *

urlpatterns = [
    re_path(r'^time_table/(?P<user_pk>[0-9]+)/$', AjaxTimeTable.as_view(), name="time_table"),
    path('time_table/', AjaxTimeTable.as_view(), name="requested_table"),
    re_path(r'^response_booking/$', response_booking, name="response_booking"),
]
