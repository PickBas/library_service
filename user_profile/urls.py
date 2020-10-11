"""user_profile urls.py"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from user_profile import views

urlpatterns = [
    path('profile/<int:pk>/', login_required(views.ProfilePageView.as_view()),
         name='profile_main_page'),
    path('librarian/stats/<int:pk>/', login_required(views.LibrarianStatsView.as_view()),
         name='librarian_stats_page'),
    path('profile/update/avatar/', login_required(views.AvatarUpdateView.as_view()),
         name='update_profile_avatar'),
    path('profile/update/profile/', login_required(views.ProfileUpdateView.as_view()),
         name='update_profile_info')
]
