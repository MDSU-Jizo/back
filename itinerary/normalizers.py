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
            'id': itinerary['id'],
            'title': itinerary['title'],
            'country': itinerary['country'],
            'starting_city': itinerary['starting_city'],
            'ending_city': itinerary['ending_city'],
            'start_date': itinerary['start_date'],
            'end_date': itinerary['end_date'],
            'multiple_cities': itinerary['multiple_cities'],
            'steps': itinerary['steps']
            if itinerary['steps'] is not None
            else 'null',
            'created_at': itinerary['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': itinerary['updated_at'].strftime('%Y-%m-%d %H:%M:%S'),
            'level': itinerary['level_id']
            if itinerary['level_id'] is not None
            else 'null',
            'user': itinerary['user_id']
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
    return {
        'id': itinerary.id,
        'title': itinerary.title,
        'country': itinerary.country,
        'starting_city': itinerary.starting_city,
        'ending_city': itinerary.ending_city,
        'start_date': itinerary.start_date,
        'end_date': itinerary.end_date,
        'multiple_cities': itinerary.multiple_cities,
        'steps': itinerary.steps
        if itinerary.steps is not None
        else 'null',
        'created_at': itinerary.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': itinerary.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'level': itinerary.level
        if itinerary.level is not None
        else 'null',
        'user': itinerary.user.id,
        'response': itinerary.response
    }
