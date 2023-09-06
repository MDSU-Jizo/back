from django import forms
from .models import FakeEntity

class FakeEntityForm(forms.ModelForm):
    class Meta:
        model = FakeEntity
        fields = (
            'title',
            'text',
        )