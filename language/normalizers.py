"""
    Language normalizers
"""


def languages_normalizer(languages):
    """
        Function to return languages as formatted data

        Args:
            languages (list): list of languages
        Returns:
            result: languages as a list of dict
    """
    result = []

    for language in languages:
        item = {
            'id': language['id'],
            'label': language['label'],
            'shortened': language['shortened'],
            'isActivate': language['is_activate'],
        }

        result.append(item)

    return result


def language_normalizer(language):
    """
        Function to return language as formatted data

        Args:
            language (object):
        Returns:
            result: language as dict
    """
    return {
        'id': language.id,
        'label': language.label
    }
