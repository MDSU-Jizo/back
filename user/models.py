"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses

from django.db import models
from contract.constants import Constants


class User(models.Model):
    """Class representing the User entity"""
    firstname = models.CharField(max_length=255, null=False)
    lastname = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    birthdate = models.DateField(null=False)
    gender = models.CharField(max_length=10, choices=Constants.GENDER_CHOICES, default=1, null=False)
    country = models.CharField(max_length=255, null=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)
    languageId = models.ForeignKey('language.Language', on_delete=models.CASCADE, default=1)
    roleId = models.ForeignKey(
        'role.Role',
        on_delete=models.CASCADE,
        default=Constants.Roles.ROLE_USER
    )

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'user'
