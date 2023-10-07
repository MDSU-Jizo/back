from .models import Level


def levels_normalizer(levels):
    """
        Function to return levels as formatted data

        Args:
            levels: list of levels
        Returns:
            result: levels as a list of dict
    """
    result = []

    for level in levels:
        print(level)
        item = {
            'id': level['id'],
            'label': level['label'],
            'isActivate': level['is_activate'],
        }

        result.append(item)

    return result


def level_normalizer(level):
    return {
        'id': level.id,
        'label': level.label
    }
