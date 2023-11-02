"""
    Itinerary forms
"""
import dataclasses

from django import forms
from .models import Itinerary


class ItineraryForm(forms.ModelForm):
    """
        Form for Level entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = Itinerary
        fields = (
            'country',
            'starting_city',
            'ending_city',
            'start_date',
            'end_date',
            'multiple_cities',
            'steps',
            'level',
            'user',
        )
