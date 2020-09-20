"""book urls.py"""

from django.urls import path

from book.views import BookListPageView, AddBookPageView, BookPageView

urlpatterns = [
    path('library/list/', BookListPageView.as_view(), name='books_list_page'),
    path('library/add/book/', AddBookPageView.as_view(), name='add_book_to_lib'),
    path('book/<int:pk>/', BookPageView.as_view(), name='book_page'),
]
