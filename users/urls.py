from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.views import *


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('complete/profile/<int:pk>/', complete_user_registration, name='complete-user'),
    path('hashTag/', hash_tags, name='hashTag'),
    path('get_field_namings/', get_registration_field_namings, name='fieldNamings'),
    path('stringMatcher/', string_matcher, name='stringMatcher'),
    path('user/profile/<int:user_pk>/', user_profile_view, name='userProfile'),
    path('user/profile_data/', get_user_profile_data, name='profile_data'),
    path('user/auto-complete/', get_names, name='auto-complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
