"""book urls.py"""

from django.urls import path

from book import views

urlpatterns = [
    path('students/all/', views.StudentsPageView.as_view(),
         name='all_students_page'),
    path('library/add/book/', views.AddBookPageView.as_view(),
         name='add_book_to_lib'),
    path('book/<int:pk>/', views.BookPageView.as_view(),
         name='book_page'),
    path('book/edit/<int:pk>/', views.EditBookPageView.as_view(),
         name='edit_book_page'),
    path('book/give/<int:pk>/', views.GiveBookPageView.as_view(),
         name='give_book_page'),
]
