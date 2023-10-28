"""
    Middleware to verify JWT authorization
"""
import os
import logging
import jwt
import re

from django.utils.deprecation import MiddlewareMixin
from contract.constants import Constants
from user.models import User
from service.api_response import send_json_response as api_response

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
unauthenticated = Constants.HttpResponseCodes.UNAUTHENTICATED


class JwtVerificationMiddleware(MiddlewareMixin):
    """
        JWT Verification Middleware Class to process a request before it reached the endpoint
    """
    _excluded_paths = [
        r'^/admin/.*$',
        r'^/user/login$',
        r'^/user/register$',
    ]

    def process_request(self, request):
        """
            Middleware handler to check JWT authentication
            Args:
                request: Request header containing authorization token

            Returns:
                JsonResponse from api_response
        """
        if self.verify_path(request):
            print('true')
            return None

        authorization = request.headers.get('authorization', None)

        if str(authorization).find("Bearer ", 0) < 0:
            return api_response(
                code=unauthenticated,
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
                        code=unauthenticated,
                        result='error',
                        message='Invalid token.',
                    )
                    logger.info("JWT VERIFICATION MIDDLEWARE RESPONSE: %s", response)

                request.jwt_token = token
                request.user_id = userid
                request.email = payload['email']

                return None
            except jwt.ExpiredSignatureError:
                response = api_response(
                    unauthenticated,
                    'error',
                    "Authentication token has expired."
                )
                logger.info("JWT VERIFICATION MIDDLEWARE RESPONSE: %s", response)

                return response
            except (jwt.DecodeError, jwt.InvalidTokenError):
                response = api_response(
                    unauthenticated,
                    'error',
                    "Authorization has failed, Please send valid token."
                )
                logger.info("JWT VERIFICATION MIDDLEWARE RESPONSE: %s", response)

                return response

        response = api_response(
            unauthenticated,
            'error',
            "Authorization not found, Please send valid token in headers."
        )
        logger.info("JWT VERIFICATION MIDDLEWARE RESPONSE: %s", response)

        return response

    def verify_path(self, request) -> bool:
        for pattern in self._excluded_paths:
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