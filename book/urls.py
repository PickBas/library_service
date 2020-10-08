"""book urls.py"""

from django.urls import path

from book.views import AddBookPageView, BookPageView, StudentsPageView, GiveBookPageView, EditBookPageView

urlpatterns = [
    path('students/all/', StudentsPageView.as_view(), name='all_students_page'),
    path('library/add/book/', AddBookPageView.as_view(), name='add_book_to_lib'),
    path('book/<int:pk>/', BookPageView.as_view(), name='book_page'),
    path('book/edit/<int:pk>/', EditBookPageView.as_view(), name='edit_book_page'),
    path('book/give/<int:pk>/', GiveBookPageView.as_view(), name='give_book_page'),
]
