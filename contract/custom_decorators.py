"""
    Custom decorators in case the app will receive a web app version
"""

import os

from django.views.decorators.csrf import csrf_exempt


def conditional_csrf_exempt(view_function):
    """
        Exempt csrf verification when .env ENV is not 'prod'
    """
    if os.getenv('ENV') != 'prod':
        return csrf_exempt(view_function)

    return view_function
