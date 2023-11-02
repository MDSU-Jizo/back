"""
    Itinerary forms
"""
import dataclasses

from django import forms
from .models import ItineraryInterest


class ItineraryInterestForm(forms.ModelForm):
    """
        Form for Level entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = ItineraryInterest
        fields = (
            'itinerary',
            'interest'
        )
