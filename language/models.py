"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class Language(models.Model):
    """Class representing the Language entity"""
    label = models.CharField(max_length=255, null=False)
    isActive = models.BooleanField(default=True, null=True, blank=True)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'language'
