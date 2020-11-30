"""book urls.py"""

from django.urls import path

from book import views

urlpatterns = [
    path('students/all/', views.StudentsPageView.as_view(),
         name='all_students_page'),
    path('librarians/all/', views.LibrariansPageView.as_view(),
         name='all_librarians_page'),
    path('library/add/book/', views.AddBookView.as_view(),
         name='add_book_post'),
    path('book/<int:pk>/', views.BookPageView.as_view(),
         name='book_page'),
    path('book/edit/<int:pk>/', views.EditBookPageView.as_view(),
         name='edit_book_page'),
    path('book/delete/<int:pk>/', views.DeleteBookView.as_view(),
         name='delete_book'),
    path('book/give/<int:pk>/', views.GiveBookView.as_view(),
         name='give_book_post'),
]
