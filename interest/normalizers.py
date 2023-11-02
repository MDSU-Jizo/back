"""
    Interest normalizers
"""


def interests_normalizer(interests):
    """
        Function to return interests as formatted data

        Args:
            interests (list): list of interests
        Returns:
            result: interests as a list of dict
    """
    result = []

    for interest in interests:
        item = {
            'id': interest['id'],
            'label': interest['label'],
            'isActivate': interest['is_activate'],
        }

        result.append(item)

    return result


def interest_normalizer(interest):
    """
        Function to return interest as formatted data

        Args:
            interest (object):
        Returns:
            result: interest as dict
    """
    return {
        'id': interest.id,
        'label': interest.label
    }
