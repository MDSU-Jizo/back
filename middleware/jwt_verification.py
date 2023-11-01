"""
    Middleware to verify JWT authorization
"""
import os
import logging
import jwt
import re

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from contract.constants import Constants
from user.models import User
from service.api_response import send_json_response as api_response

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
UNAUTHENTICATED = Constants.HttpResponseCodes.UNAUTHENTICATED
_EXCLUDED_PATHS = Constants.EXCLUDED_PATHS


class JwtVerificationMiddleware(MiddlewareMixin):
    """
        JWT Verification Middleware Class to process a request before it reached the endpoint
    """

    def process_request(self, request) -> JsonResponse | None:
        """
            Middleware handler to check JWT authentication
            Args:
                request: Request header containing authorization token

            Returns:
                JsonResponse from api_response
        """
        if self.verify_path(request):
            return None

        authorization = request.headers.get('authorization', None)

        if str(authorization).find("Bearer ", 0) < 0:
            return api_response(
                code=UNAUTHENTICATED,
                result='error',
                message='Invalid token.',
                payload=authorization
            )
        logger.info("Request received for endpoint: %s", str(request.path))

        token = str.replace(str(authorization), "Bearer ", "")

        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                userid = payload['id']
                logger.info("Request received from user: %s", userid)

                if not self.verify_user(payload):
                    response = api_response(
                        code=UNAUTHENTICATED,
                        result='error',
                        message='Invalid token.',
                    )
                    logger.info("JWT VERIFICATION MIDDLEWARE RESPONSE: %s", response)

                request.jwt_token = token
                request.user_id = userid
                request.email = payload['email']
                request.role = payload['role']

                return None
            except jwt.ExpiredSignatureError:
                response = api_response(
                    UNAUTHENTICATED,
                    'error',
                    "Authentication token has expired."
                )
                logger.info("JWT VERIFICATION MIDDLEWARE RESPONSE: %s", response)

                return response
            except (jwt.DecodeError, jwt.InvalidTokenError):
                response = api_response(
                    UNAUTHENTICATED,
                    'error',
                    "Authorization has failed, Please send valid token."
                )
                logger.info("JWT VERIFICATION MIDDLEWARE RESPONSE: %s", response)

                return response

        response = api_response(
            UNAUTHENTICATED,
            'error',
            "Authorization not found, Please send valid token in headers."
        )
        logger.info("JWT VERIFICATION MIDDLEWARE RESPONSE: %s", response)

        return response

    @staticmethod
    def verify_path(request) -> bool:
        for pattern in _EXCLUDED_PATHS:
            if re.match(pattern, request.path):
                return True
        return False

    @staticmethod
    def verify_user(token) -> bool:
        try:
            user = User.objects.filter(email=token['email'], firstname=token['firstname'], lastname=token['lastname'])
            if not user:
                return False
        except User.DoesNotExist:
            return False

        return True