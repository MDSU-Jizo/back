"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class FavoriteItinerary(models.Model):
    """Class representing the FavoriteItinerary M2M entity"""
    favorite_id = models.ForeignKey('favorite.Favorite', on_delete=models.CASCADE, null=False)
    itinerary_id = models.ForeignKey('itinerary.Itinerary', on_delete=models.CASCADE, null=False)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'favorite_itinerary'
