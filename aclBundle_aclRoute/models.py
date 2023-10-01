"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class AclBundleAclRoute(models.Model):
    """Class representing the AclBundleAclRoute M2M entity"""
    aclBundleId = models.ForeignKey('aclBundle.AclBundle', on_delete=models.CASCADE, null=False)
    aclRouteId = models.ForeignKey('aclRoute.AclRoute', on_delete=models.CASCADE, null=False)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'aclbundle_aclroute'
