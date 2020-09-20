"""book urls.py"""

from django.urls import path

from book.views import BooksPageView, AddBookPageView

urlpatterns = [
    path('library/list/', BooksPageView.as_view(), name='books_list_page'),
    path('library/add/book/', AddBookPageView.as_view(), name='add_book_to_lib'),
]