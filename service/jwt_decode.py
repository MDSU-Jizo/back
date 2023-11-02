import os
import traceback

import jwt

from django.http import JsonResponse
from datetime import date, datetime
from service.api_response import send_json_response as api_response
from contract.constants import Constants
from user.models import User

HttpCode = Constants.HttpResponseCodes


_JWT_TOKEN = os.getenv("JWT_SECRET_KEY")


def jwt_decode(authorization, secret_key=_JWT_TOKEN, algorithm="HS256") -> str | JsonResponse:
    if str(authorization).find("Bearer ", 0) < 0:
        return api_response(
            code=HttpCode.UNAUTHENTICATED,
            result='error',
            message='Invalid token.',
            payload=authorization
        )

    token = str.replace(str(authorization), "Bearer ", "")
    try:
        decode = jwt.decode(token, secret_key, algorithm)

        if verify_expiration_date(decode):
            return api_response(
                code=HttpCode.UNAUTHENTICATED,
                result='error',
                message='Token has expired.',
                user=decode['email'],
                payload=decode['expires_at'],
            )

        if not verify_user(decode):
            return api_response(
                code=HttpCode.UNAUTHENTICATED,
                result='error',
                message='Invalid token.',
                payload=traceback.print_exc()
            )
    except jwt.DecodeError:
        return api_response(
            code=HttpCode.UNAUTHENTICATED,
            result='error',
            message='An error has occurred while decoding token.',
            payload=traceback.print_exc()
        )
    except jwt.InvalidTokenError:
        return api_response(
            code=HttpCode.UNAUTHENTICATED,
            result='error',
            message='Invalid token.',
            payload=traceback.print_exc()
        )

    return decode


def verify_expiration_date(token) -> bool:
    today = date.today()

    return datetime.strptime(token['expires_at'], '%Y-%m-%d').date() < today


def verify_user(token) -> bool:
    try:
        user = User.objects.filter(email=token['email'], firstname=token['firstname'], lastname=token['lastname'])
        if not user:
            return False
    except User.DoesNotExist:
        return False

    return True