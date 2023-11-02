"""
    AclRoute forms
"""
import dataclasses

from django import forms
from .models import AclRoute


class AclRouteForm(forms.ModelForm):
    """
        Form for Level entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = AclRoute
        fields = (
            'label',
        )
