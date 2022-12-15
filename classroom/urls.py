from django.urls import path, re_path
from classroom.views import *

urlpatterns = [
    re_path(r'^time_table/(?P<user_pk>[0-9]+)/$', AjaxTimeTable.as_view(), name="time_table"),
]
