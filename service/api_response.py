"""
    Service to return pre formated JsonResponse API
"""
import logging

from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


def send_json_response(code='SUCCESS', result='', message='', data=None):
    """
    Send response in JSON format. The response is returned with code, result and data.

    Args:
        result (str, optional): Response message. Defaults to ''
        code (int, optional): Response status code. Defaults to 'SUCCESS'.
        message (str, optional): Message to display. Defaults to ''
        data (dict, optional): Response data. Defaults to {}.
    """

    if data is None:
        data = {}
    if code not in list(settings.HTTP_CONSTANTS.keys()):
        logger.error('%s code is not in responses list', code)
        code = list(settings.HTTP_CONSTANTS.keys())[0]

    if not result:
        result = code.lower()

    return JsonResponse({
        'code': settings.HTTP_CONSTANTS[code],
        'result': result,
        'message': message,
        'data': data
    })
