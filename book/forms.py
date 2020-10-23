"""book forms.py"""
from django import forms

from book.models import Book


class EditBookForm(forms.ModelForm):
    """EditBookForm form"""

    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = Book
        fields = ('name', 'info')
        widgets = {
            'info': forms.Textarea(),
        }
        labels = {
            'name': 'Название',
            'info': 'Информация о книге',
        }
