"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class Role(models.Model):
    """Class representing the Role entity"""
    label = models.CharField(max_length=100, null=False)
    is_activate = models.BooleanField(default=True, null=True, blank=True)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'role'

    def __str__(self):
        return f'id: {self.pk}, label: {self.label}, isActivate: ${self.is_activate}'
