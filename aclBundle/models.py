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


def get_acl_bundles_with_routes(activate):
    """
        Custom request to fetch every bundle with their respective routes

        Args:
            activate (bool): Filter to return bundles with is_activate set to True of False
    """
    return AclBundle.objects.raw(
        f"""
            SELECT
                b.id,
                b.label,
                b.is_activate,
                array_agg(r.label) AS routes
            FROM aclBundle AS b
            LEFT JOIN aclbundle_aclroute AS br ON br.acl_bundle_id = b.id
            LEFT JOIN aclRoute AS r ON br.acl_route_id = r.id
            WHERE b.is_activate IS {activate}
            GROUP BY b.id
            ORDER BY b.id ASC
        """
    )


def get_acl_bundle_with_routes(bundle_id):
    """
        Custom request to fetch a bundle with its respective routes

        Args:
            bundle_id (int): the id of the bundle you want to get details
    """
    return AclBundle.objects.raw(
        f"""
            SELECT
                b.id,
                b.label,
                b.is_activate,
                array_agg(r.label) AS routes
            FROM aclBundle AS b
            LEFT JOIN aclbundle_aclroute AS br ON br.acl_bundle_id = b.id
            LEFT JOIN aclRoute AS r ON br.acl_route_id = r.id
            WHERE b.id = {bundle_id}
            GROUP BY b.id
            ORDER BY b.id ASC
        """
    )
