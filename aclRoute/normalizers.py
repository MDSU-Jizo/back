"""
    AclRoute normalizers
"""


def acl_routes_normalizer(acl_routes):
    """
        Function to return acl_routes as formatted data

        Args:
            acl_routes (list): list of acl_routes
        Returns:
            result: acl_routes as a list of dict
    """
    result = []

    for acl_route in acl_routes:
        item = {
            'id': acl_route.id,
            'label': acl_route.label,
            'bundles': acl_route.bundles,
            'isActivate': acl_route.is_activate,
        }

        result.append(item)

    return result


def acl_route_normalizer(acl_route):
    """
        Function to return acl_route as formatted data

        Args:
            acl_route (list):
        Returns:
            result: acl_route as dict
    """
    for route in acl_route:
        return {
            'id': route.id,
            'label': route.label,
            'bundles': route.bundles,
            'isActivate': route.is_activate,
        }
