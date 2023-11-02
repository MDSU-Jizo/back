"""
    Level normalizers
"""


def levels_normalizer(levels):
    """
        Function to return levels as formatted data

        Args:
            levels (list): list of levels
        Returns:
            result: levels as a list of dict
    """
    result = []

    for level in levels:
        item = {
            'id': level['id'],
            'label': level['label'],
            'isActivate': level['is_activate'],
        }

        result.append(item)

    return result


def level_normalizer(level):
    """
        Function to return level as formatted data

        Args:
            level (object):
        Returns:
            result: level as dict
    """
    return {
        'id': level.id,
        'label': level.label
    }
