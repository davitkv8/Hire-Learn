from django.urls import path
from blog.views import *


urlpatterns = [
    path('', main_view, name='main-view'),
]
