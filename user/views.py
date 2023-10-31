import json
import os

import jwt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import update_last_login
from passlib.hash import pbkdf2_sha256
from datetime import date, timedelta

from service.verify_method import verify_method
from .models import User, get_list_of_users, get_user_details, encrypt_profile
from .forms import UserForm, UpdateForm, UpdateLanguage
from .normalizers import jwt_normalizer, profile_normalizer, users_normalizer, user_normalizer
from service.api_response import send_json_response as api_response
from contract.constants import Constants
from contract.custom_decorators import conditional_csrf_exempt

HttpCode = Constants.HttpResponseCodes
_KEY = os.getenv("JWT_SECRET_KEY")
_ALGORITHM = os.getenv("JWT_ALGORITHM")
_EXPIRATION = int(os.getenv("JWT_EXPIRATION"))


def encode_user_as_jwt(user, key=_KEY, algorithm=_ALGORITHM, expiration=_EXPIRATION) -> str:
    expiration_date = date.today() + timedelta(days=expiration)
    jwt_body = jwt_normalizer(user, expiration_date)

    return jwt.encode(jwt_body, key=key, algorithm=algorithm)


def register(request) -> JsonResponse:
    has_method = verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    if not request.body or json.loads(request.body) == {}:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Require a payload.',
            url=request.path,
        )

    content = json.loads(request.body.decode('utf-8'))

    if User.objects.filter(email=content['email']).exists():
        return api_response(
            code=HttpCode.NOT_ALLOWED,
            result='error',
            message='This email address already exists.',
            url=request.path,
            payload=content
        )

    if 'password' not in content:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Password required.',
            url=request.path,
            payload=content
        )

    content['password'] = pbkdf2_sha256.encrypt(content['password'])

    form = UserForm(content)
    if not form.is_valid():
        return api_response(
            code=HttpCode.INTERNAL_SERVER_ERROR,
            result='error',
            message='Invalid form.',
            data=form.errors,
            url=request.path,
            payload=content
        )

    user = form.save()
    update_last_login(None, user)
    token = encode_user_as_jwt(user)

    return api_response(code=HttpCode.CREATED, result='success', message='User created successfully.', data=token)


def login(request) -> JsonResponse:
    has_method = verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    if not request.body or json.loads(request.body) == {}:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Require a payload.',
            url=request.path,
        )

    content = json.loads(request.body.decode('utf-8'))

    if 'email' not in content:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Email required.',
            url=request.path,
            payload=content
        )

    try:
        user = User.objects.get(email=content['email'])
    except User.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Bad credentials.',
            url=request.path,
            payload=content
        )

    if 'password' not in content:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Password required.',
            url=request.path,
            payload=content
        )

    if not pbkdf2_sha256.verify(content['password'], user.password):
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Bad credentials.',
            url=request.path,
            payload=content
        )

    update_last_login(None, user)
    token = encode_user_as_jwt(user)

    return api_response(HttpCode.SUCCESS, 'success', message="Logged in successfully.", data=token)


def get_profile(request) -> JsonResponse:
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        user = User.objects.get(email=request.email)
    except User.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='User not found.', url=request.path)

    normalizer = profile_normalizer(user)

    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


def get_users(request) -> JsonResponse:
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        filter = request.GET.get('isActivate', True)
        users = get_list_of_users(filter)
    except User.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success', data=[])

    normalizer = users_normalizer(users)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


def get_user(request, user_id) -> JsonResponse:
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        user = get_user_details(user_id)
        if not user:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='User not found.',
                url=request.path
            )

    except User.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='User not found.',
            url=request.path
        )

    normalizer = user_normalizer(user)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


def update_profile(request, user_id) -> JsonResponse:
    has_method = verify_method(expected_method='PATCH', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    if not request.body or json.loads(request.body) == {}:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Require a payload.',
            url=request.path,
        )

    content = json.loads(request.body.decode('utf-8'))

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='User not found.',
            url=request.path
        )

    if request.user_id != user_id:
        return api_response(
            code=HttpCode.FORBIDDEN,
            result='error',
            message='You don\'t have the right to modify this profile.',
            url=request.path,
        )

    form = UpdateForm(instance=user, data=content)
    if not form.is_valid():
        return api_response(
            code=HttpCode.INTERNAL_SERVER_ERROR,
            result='error',
            message='Invalid form.',
            data=form.errors,
            url=request.path,
            payload=content
        )

    form.save()
    token = encode_user_as_jwt(user)

    return api_response(HttpCode.SUCCESS, 'success', message='User updated successfully.', data=token)


def update_password(request, user_id) -> JsonResponse:
    has_method = verify_method(expected_method='PATCH', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    if not request.body or json.loads(request.body) == {}:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Require a payload.',
            url=request.path,
        )

    if request.user_id != user_id:
        return api_response(
            code=HttpCode.FORBIDDEN,
            result='error',
            message='You don\'t have the right to modify this profile.',
            url=request.path,
        )

    content = json.loads(request.body.decode('utf-8'))

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='User not found.',
            url=request.path
        )

    missing_key = ''
    if 'actualPassword' not in content:
        missing_key = 'actualPassword'
    elif 'newPassword' not in content:
        missing_key = 'newPassword'
    elif 'confirmPassword' not in content:
        missing_key = 'confirmPassword'

    if missing_key != '':
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Invalid form.',
            data=f'{missing_key} is required.',
            url=request.path,
        )

    verify_password = pbkdf2_sha256.verify(content['actualPassword'], user.password)
    if not verify_password:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Incorrect actual password.',
            url=request.path,
            payload=content
        )

    if content['newPassword'] != content['confirmPassword']:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Passwords don\'t match.',
            url=request.path,
            payload=content
        )

    new_password = pbkdf2_sha256.encrypt(content['newPassword'])
    user.password = new_password
    user.save()

    return api_response(HttpCode.SUCCESS, 'success', message='Password updated successfully.')


def delete_profile(request, user_id) -> JsonResponse:
    has_method = verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='User not found.',
            url=request.path
        )

    if request.user_id != user_id:
        return api_response(
            code=HttpCode.FORBIDDEN,
            result='error',
            message='You don\'t have the right to modify this profile.',
            url=request.path,
        )

    encrypt_profile(user)

    return api_response(HttpCode.SUCCESS, 'success', message='Profile deleted successfully.')


def change_language(request, user_id) -> JsonResponse:
    has_method = verify_method(expected_method='PATCH', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    if not request.body or json.loads(request.body) == {}:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Require a payload.',
            url=request.path,
        )

    content = json.loads(request.body.decode('utf-8'))

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='User not found.',
            url=request.path
        )

    if request.user_id != user_id:
        return api_response(
            code=HttpCode.FORBIDDEN,
            result='error',
            message='You don\'t have the right to modify this profile.',
            url=request.path,
        )

    form = UpdateLanguage(instance=user, data=content)
    if not form.is_valid():
        return api_response(
            code=HttpCode.INTERNAL_SERVER_ERROR,
            result='error',
            message='Invalid form.',
            data=form.errors,
            url=request.path,
            payload=content
        )

    form.save()
    token = encode_user_as_jwt(user)

    return api_response(HttpCode.SUCCESS, 'success', message='Language updated successfully.', data=token)
