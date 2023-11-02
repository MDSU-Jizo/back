"""
    AclBundle forms
"""
import dataclasses

from django import forms
from .models import AclBundle


class AclBundleForm(forms.ModelForm):
    """
        Form for Level entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = AclBundle
        fields = (
            'label',
        )
