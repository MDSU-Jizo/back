"""
    Type forms
"""
import dataclasses

from django import forms
from .models import Type


class TypeForm(forms.ModelForm):
    """
        Form for Level entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = Type
        fields = (
            'label',
        )
