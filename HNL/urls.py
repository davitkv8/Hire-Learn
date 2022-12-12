"""HNL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from blog.views import main_view

from users.views import Login, register,\
    complete_user_registration, hash_tags,\
    get_registration_field_namings, string_matcher,\
    user_profile_view, get_user_profile_data, get_names


urlpatterns = [
    path('admin/', admin.site.urls),

    # BLOG APP
    path('', main_view, name='main-view'),

    # USERS APP
    path('login/', Login.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('complete/profile/<int:pk>/', complete_user_registration, name='complete-user'),
    path('hashTag/', hash_tags, name='hashTag'),
    path('get_field_namings/', get_registration_field_namings, name='fieldNamings'),
    path('stringMatcher/', string_matcher, name='stringMatcher'),
    path('user/profile/<int:user_pk>/', user_profile_view, name='userProfile'),
    path('user/profile_data/', get_user_profile_data, name='profile_data'),
    path('user/auto-complete/', get_names, name='auto-complete')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
