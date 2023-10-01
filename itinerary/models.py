"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class Itinerary(models.Model):
    """Class representing the Itinerary entity"""
    country = models.CharField(max_length=255, null=False)
    startLocation = models.CharField(max_length=255, null=False)
    endLocation = models.CharField(max_length=255, null=True, blank=True)
    startDate = models.DateField(null=False)
    endDate = models.DateField(null=False)
    steps = models.JSONField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)
    level_id = models.ForeignKey('level.Level', on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'itinerary'
