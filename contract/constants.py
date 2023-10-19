"""
    File used to enumerate Http response codes
"""
import dataclasses
from enum import Enum


class Constants:
    """
        Class with every constant used in the app
    """

    GENDER_CHOICES = [
        (1, "Male"),
        (2, "Female"),
        (3, "Other"),
    ]

    class HttpResponseCodes(Enum):
        """
            Http response codes enum
        """
        SUCCESS = 200
        CREATED = 201
        BAD_REQUEST = 400
        UNAUTHENTICATED = 401
        FORBIDDEN = 403
        NOT_FOUND = 404
        NOT_ALLOWED = 405
        INTERNAL_SERVER_ERROR = 500

    class Roles(Enum):
        """
            User roles id enum
        """
        ROLE_USER = 1
        ROLE_PREMIUM = 2
        ROLE_ADMIN = 3
        ROLE_SUPER_ADMIN = 4

    class Types(Enum):
        """
            Type id enum
        """
        TOURISM = 1
        ROADTRIP = 2
        BACKPACKING = 3
        HIKING = 4
        DISCOVERING = 5
