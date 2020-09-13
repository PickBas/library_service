"""core urls.py"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from core.views import IndexPageView

urlpatterns = [
    path('', login_required(IndexPageView.as_view()))
]
