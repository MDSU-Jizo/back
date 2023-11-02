"""
    Itinerary normalizers
"""


def itineraries_normalizer(itineraries):
    """
        Function to return itineraries as formatted data

        Args:
            itineraries (list): list of itineraries
        Returns:
            result: itineraries as a list of dict
    """
    result = []

    for itinerary in itineraries:
        item = {
            'id': itinerary.id,
            'title': itinerary.title,
            'country': itinerary.country,
            'starting_city': itinerary.starting_city,
            'ending_city': itinerary.ending_city,
            'start_date': itinerary.start_date,
            'end_date': itinerary.end_date,
            'types': itinerary.types,
            'interests': itinerary.interests,
            'multiple_cities': itinerary.multiple_cities,
            'steps': itinerary.steps
            if itinerary.steps is not None
            else None,
            'created_at': itinerary.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': itinerary.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'level': {
                'id': itinerary.level.id,
                'label': itinerary.level.label
            } if itinerary.level is not None else None,
            'user': {
                'id': itinerary.user.id,
                'display_name': itinerary.user.firstname + " " + itinerary.user.lastname,
                'email': itinerary.user.email,
            },
        }

        result.append(item)

    return result


def itinerary_normalizer(itinerary):
    """
        Function to return itinerary as formatted data

        Args:
            itinerary (object):
        Returns:
            result: itinerary as dict
    """
    for data in itinerary:
        return {
            'id': data.id,
            'title': data.title,
            'country': data.country,
            'starting_city': data.starting_city,
            'ending_city': data.ending_city,
            'start_date': data.start_date,
            'end_date': data.end_date,
            'types': data.types,
            'interests': data.interests,
            'multiple_cities': data.multiple_cities,
            'steps': data.steps
            if data.steps is not None
            else None,
            'created_at': data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': data.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'level': {
                'id': data.level.id,
                'label': data.level.label,
            } if data.level is not None else None,
            'user': {
                'id': data.user.id,
                'display_name': data.user.firstname + " " + data.user.lastname,
                'email': data.user.email,
            },
            'response': data.response
        }
