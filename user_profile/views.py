"""user_profile views.py"""
from django.contrib.auth.models import User
from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.views import View


class ProfilePageView(View):
    """ProfilePageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'profile/profile_main_page.html'
        self.context = {}
        self.current_user = None
        super(ProfilePageView, self).__init__(**kwargs)

    def get(self, request: HttpRequest, **kwargs: dict) -> render:
        """
        Processing GET request.

        :param request: HttpRequest
        :param kwargs: dict (pk)
        :returns: render
        :raises: Http404
        """

        if not User.objects.filter(id=kwargs['pk']).exists():
            raise Http404()

        self.current_user = User.objects.get(id=kwargs['pk'])
        self.context['current_user'] = self.current_user
        self.context['page_name'] = self.current_user.username

        return render(request, self.template_name, self.context)
