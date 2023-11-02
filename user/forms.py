"""
    User forms
"""
import dataclasses

from django import forms
from .models import User


class UserForm(forms.ModelForm):
    """
        Form for User entity
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = User
        fields = (
            'firstname',
            'lastname',
            'email',
            'password',
        )
        widgets = {
            'password': forms.PasswordInput()
        }


class LoginForm(forms.ModelForm):
    """
        Form for User login
    """
    @dataclasses.dataclass
    class Meta:
        """
            Metaclass for the form
        """
        model = User
        fields = (
            'email',
            'password',
        )
        widgets = {
            'password': forms.PasswordInput(),
        }


class UpdateForm(forms.ModelForm):
    @dataclasses.dataclass
    class Meta:
        model = User
        exclude = ('firstname', 'password')
        fields = (
            'lastname',
            'email',
            'birthdate',
            'gender',
            'country'
        )


class UpdateLanguage(forms.ModelForm):
    @dataclasses.dataclass
    class Meta:
        model = User
        fields = (
            'language',
        )
