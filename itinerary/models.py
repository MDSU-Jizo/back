"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class Itinerary(models.Model):
    """Class representing the Itinerary entity"""
    country = models.CharField(max_length=255, null=False)
    start_location = models.CharField(max_length=255, null=False)
    end_location = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    steps = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    level = models.ForeignKey('level.Level', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'itinerary'
