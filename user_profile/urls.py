"""user_profile urls.py"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from user_profile.views import ProfilePageView, AvatarUpdateView, ProfileUpdateView

urlpatterns = [
    path('profile/<int:pk>/', login_required(ProfilePageView.as_view()),
         name='profile_main_page'),
    path('profile/update/avatar/', login_required(AvatarUpdateView.as_view()),
         name='update_profile_avatar'),
    path('profile/update/profile/', login_required(ProfileUpdateView.as_view()),
         name='update_profile_info')
]

