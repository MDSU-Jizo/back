"""
    Role forms
"""
import dataclasses

from django import forms
from .models import Role


class RoleForm(forms.ModelForm):
    """
        Form for Level entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = Role
        fields = (
            'label',
        )
