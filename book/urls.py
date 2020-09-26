"""book urls.py"""

from django.urls import path

from book.views import AddBookPageView, BookPageView, StudentsPageView

urlpatterns = [
    path('students/all/', StudentsPageView.as_view(), name='all_students_page'),
    path('library/add/book/', AddBookPageView.as_view(), name='add_book_to_lib'),
    path('book/<int:pk>/', BookPageView.as_view(), name='book_page'),
]
