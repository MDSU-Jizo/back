"""
    Language forms
"""
import dataclasses

from django import forms
from .models import Language


class LanguageForm(forms.ModelForm):
    """
        Form for Language entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = Language
        fields = (
            'label',
        )
