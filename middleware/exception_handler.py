"""
    Middleware used to catch exceptions
"""
import traceback
import logging

from django.conf import settings
from service.api_response import send_json_response as api_response


class ExceptionHandlerMiddleware:
    """
        Error Handler Middleware

        Return the exception
        If DEBUG=False, log the error for ELK to fetch it
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """
            Return exception,
            If DEBUG=False, log th error for ELF to fetch it
        """
        message = ''
        if exception:
            if not settings.DEBUG:
                message = '**{url}**\n\n{error}\n\n````{tb}````'.format(
                    url=request.build_absolute_uri(),
                    error=repr(exception),
                    tb=traceback.format_exc()
                )

                logging.error(
                    'RAISING EXCEPTION, CODE: %s,\n MESSAGE: %s',
                    self.get_response.status_code,
                    message
                )

        return api_response(code=self.get_response.status_code, result='error', data=message)
