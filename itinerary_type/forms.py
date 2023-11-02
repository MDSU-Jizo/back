"""
    Type forms
"""
import dataclasses

from django import forms
from .models import ItineraryType


class ItineraryTypeForm(forms.ModelForm):
    """
        Form for Level entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = ItineraryType
        fields = (
            'itinerary',
            'type'
        )
