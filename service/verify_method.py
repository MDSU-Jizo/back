"""
    Request method verification
"""
from contract.constants import Constants
from .api_response import send_json_response as api_response


def verify_method(expected_method, requested_method, requested_path):
    """
        Function to verify request method

        Args:
            expected_method (str): 'GET', 'POST', ...
            requested_method (str): Method fetched from request
            requested_path (str): View path to send in api_response if requested_method does not match

        Returns:
            JsonResponse if the args do not match
            True if the args match
    """
    if requested_method != expected_method:
        return api_response(
            code=Constants.HttpResponseCodes.BAD_REQUEST,
            result='error',
            message=f'Must be a ${expected_method} method.',
            url=requested_path
        )

    return True
