"""
    AclBundle normalizers
"""


def acl_bundles_normalizer(acl_bundles):
    """
        Function to return acl_bundles as formatted data

        Args:
            acl_bundles (list): list of acl_bundles
        Returns:
            result: acl_bundles as a list of dict
    """
    result = []

    for acl_bundle in acl_bundles:
        item = {
            'id': acl_bundle['id'],
            'label': acl_bundle['label'],
            'isActivate': acl_bundle['is_activate'],
        }

        result.append(item)

    return result


def acl_bundle_normalizer(acl_bundle):
    """
        Function to return acl_bundle as formatted data

        Args:
            acl_bundle (object):
        Returns:
            result: acl_bundle as dict
    """
    return {
        'id': acl_bundle.id,
        'label': acl_bundle.label
    }
