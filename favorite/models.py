"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class Favorite(models.Model):
    """Class representing the Favorite entity"""
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)
    isActive = models.BooleanField(default=True, null=True, blank=True)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'favorite'
