"""library urls.py"""

from django.urls import path

from library.views import BooksPageView

urlpatterns = [
    path('library/list/', BooksPageView.as_view(), name='books_list_page')
]
