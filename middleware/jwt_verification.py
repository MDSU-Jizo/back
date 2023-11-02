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
                payload=authorization,
                url=request.path
            )

        token = str.replace(str(authorization), "Bearer ", "")

        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                userid = payload['id']

                if not self.verify_user(payload):
                    response = api_response(
                        code=UNAUTHENTICATED,
                        result='error',
                        message='Invalid token.',
                        payload=payload,
                        user=userid,
                        url=request.path
                    )

                    return response

                request.jwt_token = token
                request.user_id = userid
                request.email = payload['email']
                request.role = payload['role']

                return None
            except jwt.ExpiredSignatureError:
                response = api_response(
                    code=UNAUTHENTICATED,
                    result='error',
                    message="Authentication token has expired.",
                    payload=token,
                    url=request.path
                )

                return response
            except (jwt.DecodeError, jwt.InvalidTokenError):
                response = api_response(
                    code=UNAUTHENTICATED,
                    result='error',
                    message="Authorization has failed, Please send valid token.",
                    payload=token,
                    url=request.path
                )

                return response

        response = api_response(
            code=UNAUTHENTICATED,
            result='error',
            message="Authorization not found, Please send valid token in headers.",
            payload=authorization,
            url=request.path
        )

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
