# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django import forms

from .models import Item
EMPTY_LIST_ERROR = "You can't have an empty list item"


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control input-lg'
                }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }
