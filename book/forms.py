"""book forms.py"""
from django import forms


class UploadBookForm(forms.Form):
    """UploadBookForm form"""
    file = forms.FileField(required=True, help_text="Загрузить книгу")