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
    is_activate = models.BooleanField(default=True, null=True, blank=True)

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
                title = f"{self.starting_city}"
            else:
                title = f"{self.starting_city} - {self.ending_city}"
            self.title = title

        super().save()


def get_itineraries_with_types_and_interests(activate):
    return Itinerary.objects.raw(
        f"""
            SELECT 
                i.*,
                (
                    SELECT array_agg(inte.label)
                    FROM interest as inte
                    WHERE inte.id IN (
                        SELECT iin.interest_id
                        FROM itinerary_interest AS iin
                        WHERE iin.itinerary_id = i.id
                    )
                ) AS interests,
                (
                    SELECT array_agg(type.label)
                    FROM type
                    WHERE type.id IN (
                        SELECT it.type_id
                        FROM itinerary_type AS it
                        WHERE it.itinerary_id = i.id
                    )
                ) AS types
            FROM itinerary AS i
            WHERE i.is_activate = {activate}
            GROUP BY i.id
        """
    )


def get_user_itineraries_with_types_and_interests(user_id, activate):
    return Itinerary.objects.raw(
        f"""
            SELECT 
                i.*,
                (
                    SELECT array_agg(inte.label)
                    FROM interest as inte
                    WHERE inte.id IN (
                        SELECT iin.interest_id
                        FROM itinerary_interest AS iin
                        WHERE iin.itinerary_id = i.id
                    )
                ) AS interests,
                (
                    SELECT array_agg(type.label)
                    FROM type
                    WHERE type.id IN (
                        SELECT it.type_id
                        FROM itinerary_type AS it
                        WHERE it.itinerary_id = i.id
                    )
                ) AS types
            FROM itinerary AS i
            WHERE i.user_id = {user_id}
            AND i.is_activate = {activate}
            GROUP BY i.id
        """
    )


def get_itinerary_with_types_and_interests(interest_id, activate):
    return Itinerary.objects.raw(
        f"""
            SELECT 
                i.*,
                (
                    SELECT array_agg(inte.label)
                    FROM interest as inte
                    WHERE inte.id IN (
                        SELECT iin.interest_id
                        FROM itinerary_interest AS iin
                        WHERE iin.itinerary_id = i.id
                    )
                ) AS interests,
                (
                    SELECT array_agg(type.label)
                    FROM type
                    WHERE type.id IN (
                        SELECT it.type_id
                        FROM itinerary_type AS it
                        WHERE it.itinerary_id = i.id
                    )
                ) AS types
            FROM itinerary AS i
            WHERE i.id = {interest_id}
            AND i.is_activate = {activate}
            GROUP BY i.id
        """
    )


def count_user_itineraries(user_id):
    return Itinerary.objects.raw(
        f"""
            SELECT
                COUNT(i.*)
            FROM itinerary AS i 
            WHERE i.user_id = {user_id}
        """
    )
