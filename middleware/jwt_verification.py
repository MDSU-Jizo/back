"""
    Middleware to verify JWT authorization
"""
import logging
import jwt
from django.conf import settings
from environ import Env
from service.api_response import send_json_response as api_response

logger = logging.getLogger(__name__)

env = Env()
env.read_env()
SECRET_KEY = env("JWT_SECRET_KEY")
unauthenticated = settings.HTTP_CONSTANTS['UNAUTHENTICATED']


class JwtVerificationMiddleware:
    """
        JWT Verification Middleware Class to process a request before it reached the endpoint
    """
    def process_request(self, request):
        """
            Middleware handler to check JWT authentication
            Args:
                request: Request header containing authorization token

            Returns:
                JsonResponse from api_response
        """
        jwt_token = request.headers.get('authorization', None)
        logger.info("Request received for endpoint: %s", str(request.path))

        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
                userid = payload['user_id']
                logger.info("Request received from user: %s", userid)

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
