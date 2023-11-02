"""
    Interest forms
"""
import dataclasses

from django import forms
from .models import Interest


class InterestForm(forms.ModelForm):
    """
        Form for Interest entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = Interest
        fields = (
            'label',
        )
