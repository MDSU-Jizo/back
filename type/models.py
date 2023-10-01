"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class Type(models.Model):
    """Class representing the Type entity"""
    label = models.CharField(max_length=255, null=False)
    isActive = models.BooleanField(default=True, null=True, blank=True)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'type'
