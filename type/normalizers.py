"""
    Type normalizers
"""


def types_normalizer(types):
    """
        Function to return types as formatted data

        Args:
            types (list): list of types
        Returns:
            result: types as a list of dict
    """
    result = []

    for type in types:
        item = {
            'id': type['id'],
            'label': type['label'],
            'isActivate': type['is_activate'],
        }

        result.append(item)

    return result


def type_normalizer(type):
    """
        Function to return type as formatted data

        Args:
            type (object):
        Returns:
            result: type as dict
    """
    return {
        'id': type.id,
        'label': type.label
    }
