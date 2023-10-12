"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class ItineraryType(models.Model):
    """Class representing the ItineraryType M2M entity"""
    itinerary = models.ForeignKey('itinerary.Itinerary', on_delete=models.CASCADE, null=False)
    type = models.ForeignKey('type.Type', on_delete=models.CASCADE, null=False)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'itinerary_type'
