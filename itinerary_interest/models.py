"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class ItineraryInterest(models.Model):
    """Class representing the ItineraryInterest M2M entity"""
    itineraryId = models.ForeignKey('itinerary.Itinerary', on_delete=models.CASCADE, null=False)
    interestId = models.ForeignKey('interest.Interest', on_delete=models.CASCADE, null=False)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'itinerary_interest'
