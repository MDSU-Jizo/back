"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class Itinerary(models.Model):
    """Class representing the Itinerary entity"""
    title = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=False)
    starting_city = models.CharField(max_length=255, null=False)
    ending_city = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    multiple_cities = models.BooleanField(default=False, null=True, blank=True)
    steps = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    level = models.ForeignKey('level.Level', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)
    response = models.JSONField(null=True, blank=True)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'itinerary'
        verbose_name_plural = 'itineraries'

    def __str__(self):
        return f"""
        id: {self.pk},
        Country: {self.country}, 
        Starting city: {self.starting_city}, 
        Ending city: {self.ending_city}, 
        User: {self.user}
    """

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        if not self.ending_city:
            self.ending_city = self.starting_city
        if not self.title:
            if self.ending_city == self.starting_city:
                title = f"{self.starting_city} ({self.start_date} - {self.end_date})"
            else:
                title = f"{self.starting_city} - {self.ending_city} ({self.start_date} - {self.end_date})"
            self.title = title

        super().save()
