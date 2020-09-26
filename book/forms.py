"""book forms.py"""
from django import forms


class UploadBookForm(forms.Form):
    """UploadBookForm form"""

    name = forms.CharField(max_length=100,
                           label='Название')
