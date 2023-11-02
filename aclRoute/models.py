"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class AclRoute(models.Model):
    """Class representing the AclRoute entity"""
    label = models.CharField(max_length=255, null=False)
    is_activate = models.BooleanField(default=True, null=True, blank=True)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'aclroute'

    def __str__(self):
        return f'id: {self.pk}, label: {self.label}, isActivate: {self.is_activate}'


def get_acl_routes_with_bundles(activate):
    """
        Custom request to fetch every route with their respective bundles

        Args:
            activate (bool): Filter to return bundles with is_activate set to True of False
    """
    return AclRoute.objects.raw(
        f"""
            SELECT
                r.id,
                r.label,
                r.is_activate,
                array_agg(b.label) AS bundles
            FROM aclroute AS r
            LEFT JOIN aclbundle_aclroute AS br ON br.acl_route_id = r.id
            LEFT JOIN aclbundle AS b ON br.acl_bundle_id = b.id
            WHERE r.is_activate IS {activate}
            GROUP BY r.id
            ORDER BY r.id ASC    
        """
    )


def get_acl_route_with_bundles(route_id):
    """
        Custom request to fetch a bundle with its respective routes

        Args:
            route_id (int): the id of the bundle you want to get details
    """
    return AclRoute.objects.raw(
        f"""
            SELECT
                r.id,
                r.label,
                r.is_activate,
                array_agg(b.label) AS bundles
            FROM aclroute AS r
            LEFT JOIN aclbundle_aclroute AS br ON br.acl_route_id = r.id
            LEFT JOIN aclbundle AS b ON br.acl_bundle_id = b.id
            WHERE r.id = {route_id}
            GROUP BY r.id
            ORDER BY r.id ASC    
        """
    )
