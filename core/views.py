"""Core views.py"""
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from book.models import Book


class IndexPageView(View):
    """IndexPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'core/index.html'
        self.context = {'page_name': 'Список книг'}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing get request

        :param request: HttpRequest
        :return: render
        """
        
        self.context['books'] = Book.objects.all()
        return render(request, self.template_name, self.context)
