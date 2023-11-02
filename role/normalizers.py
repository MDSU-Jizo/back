"""
    Role normalizers
"""


def roles_normalizer(roles):
    """
        Function to return roles as formatted data

        Args:
            roles (list): list of roles
        Returns:
            result: roles as a list of dict
    """
    result = []

    for role in roles:
        item = {
            'id': role['id'],
            'label': role['label'],
            'isActivate': role['is_activate'],
        }

        result.append(item)

    return result


def role_normalizer(role):
    """
        Function to return role as formatted data

        Args:
            role (object):
        Returns:
            result: role as dict
    """
    return {
        'id': role.id,
        'label': role.label
    }
