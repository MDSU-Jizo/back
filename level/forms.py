"""
    Level forms
"""
import dataclasses

from django import forms
from .models import Level


class LevelForm(forms.ModelForm):
    """
        Form for Level entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = Level
        fields = (
            'label',
        )
