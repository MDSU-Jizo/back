"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class Favorite(models.Model):
    """Class representing the Favorite entity"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)
    is_activate = models.BooleanField(default=True, null=True, blank=True)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'favorite'

    def __str__(self):
        return f'User id: {self.user}, isActivate: {self.is_activate}'
