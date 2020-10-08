"""core admin.py"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from book.models import Book

UserAdmin.list_display = ('email', 'first_name', 'last_name',
                          'is_active', 'date_joined', 'is_staff')

UserAdmin.readonly_fields = ('first_name', 'last_name', 'email', 'username')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ['since_given', 'since_back', 'when_should_be_back',
                       'in_use_by', 'read_history']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
