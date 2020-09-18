"""user_profile urls.py"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from user_profile.views import ProfilePageView

urlpatterns = [
    path('profile/<int:pk>/', login_required(ProfilePageView.as_view()),
         name='profile_main_page')
]

