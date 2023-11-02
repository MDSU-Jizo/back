"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
from django.db import models


class RoleAclBundle(models.Model):
    """Class representing the RoleAclBundle M2M entity"""
    role = models.ForeignKey('role.Role', on_delete=models.CASCADE, null=False)
    acl_bundle = models.ForeignKey('aclBundle.AclBundle', on_delete=models.CASCADE, null=False)

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'role_aclbundle'

    def __str__(self):
        return f'Role: {self.role}, aclBundle: {self.acl_bundle}'
