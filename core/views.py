"""Core views.py"""
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from user_profile.models import Profile


class IndexPageView(View):
    """IndexPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'core/index.html'
        self.context = {'page_name': 'Main page'}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing get request

        :param request: HttpRequest
        :return: render
        """

        all_users = User.objects.filter(profile__is_student=True)
        self.context['all_users'] = all_users

        return render(request, self.template_name, self.context)
