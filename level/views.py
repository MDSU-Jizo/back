"""
    Level views
"""
import json

from django.http import JsonResponse
from .models import Level
from .normalizers import levels_normalizer, level_normalizer
from .forms import LevelForm
from service.api_response import send_json_response as api_response
from service.verify_method import verify_method
from contract.constants import Constants

HttpCode = Constants.HttpResponseCodes


def get_levels(request):
    """
        Function to fetch every level from database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
        Filter:
            isActivate (False, optional with default value to True): Fetched from request url parameter.
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    filter = request.GET.get('isActivate', True)
    try:
        levels = Level.objects.all().values().filter(is_activate=filter)
    except Level.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success')

    normalizer = levels_normalizer(levels)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


def get_level(request, level_id):
    """
        Function to fetch every level from database

        Args:
            request: Request header containing authorization and method
            level_id (int): id of the level
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        level = Level.objects.get(pk=level_id)

        if not level:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Level not found.', url=request.path)
    except Level.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Level not found.', url=request.path)

    normalizer = level_normalizer(level)
    return api_response(code=HttpCode.SUCCESS, result='success', data=normalizer)


def add_level(request):
    """
        Function to add a level in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    content = json.loads(request.body.decode('utf-8'))
    form = LevelForm(content)
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
    return api_response(code=HttpCode.CREATED, result='success', message='Level created successfully.')


def update_level(request):
    """
        Function to update a level in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='PATCH', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    content = json.loads(request.body.decode('utf-8'))

    try:
        level = Level.objects.get(pk=content['id'])
        if not level:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Level not found.',
                url=request.path,
                payload=content
            )
    except Level.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Level not found.',
            url=request.path,
            payload=content
        )

    form = LevelForm(instance=level, data=content)
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
    return api_response(code=HttpCode.SUCCESS, result='success', message='Level updated successfully.')


def delete_level(request, level_id):
    """
        Function to set is_active to False on a level in database

        Args:
            request: Request header containing authorization and method
            level_id: id of the level
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        level = Level.objects.get(pk=level_id)

        if not level:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Level not found.', url=request.path)
    except Level.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Level not found.', url=request.path)

    level.is_activate = False
    level.save()
    return api_response(code=HttpCode.SUCCESS, result='success', message='Level deleted successfully.')
