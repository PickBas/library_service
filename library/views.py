"""library views.py"""
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class BooksPageView(View):
    """BooksPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/books_list.html'
        self.context = {'page_name': 'Список книг в библиотеке'}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :returns: render
        """

        return render(request, self.template_name, self.context)
