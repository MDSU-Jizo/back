"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class AclBundle(models.Model):
    """Class representing the AclBundle entity"""
    label = models.CharField(max_length=255, null=False)
    is_activate = models.BooleanField(default=True, null=True, blank=True)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'aclbundle'

    def __str__(self):
        return f'id: {self.pk}, label: {self.label}, isActivate: ${self.is_activate}'