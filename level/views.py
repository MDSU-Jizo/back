import json

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Level
from .normalizer import levels_normalizer, level_normalizer
from .form import LevelForm
from service.api_response import send_json_response as api_response
from service.verify_method import verify_method
from contract.constants import Constants

http_codes = Constants.HttpResponseCodes


def get_levels(request):
    """
        Function to fetch every level from database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
        Filter:
            filter (False, optional with default value to True): Fetched from request url parameter.
    """
    verify_method('GET', request.method, requested_path=request.path)

    filter = request.GET.get('filter', True)
    try:
        levels = Level.objects.all().values().filter(is_activate=filter)
    except Level.DoesNotExist:
        return api_response(http_codes.SUCCESS, 'success', data=[])

    normalizer = levels_normalizer(levels)
    return api_response(http_codes.SUCCESS, 'success', data=normalizer)


def get_level(request, level_id):
    """
        Function to fetch every level from database

        Args:
            request: Request header containing authorization and method
            level_id (int): id of the level
        Returns:
            JsonResponse containing request's information
    """
    verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)

    try:
        level = Level.objects.get(pk=level_id)

        if not level:
            return api_response(code=http_codes.NOT_FOUND, result='error', message='Level not found.', url=request.path)
    except Level.DoesNotExist:
        return api_response(code=http_codes.NOT_FOUND, result='error', message='Level not found.', url=request.path)

    normalizer = level_normalizer(level)
    return api_response(code=http_codes.SUCCESS, result='success', data=normalizer)

@csrf_exempt
def add_level(request):
    verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)

    content = json.loads(request.body.decode('utf-8'))
    form = LevelForm(content)
    if not form.is_valid():
        return api_response(
            code=http_codes.INTERNAL_SERVER_ERROR,
            result='error',
            message='Invalid form.',
            data=form.errors,
            url=request.path,
            payload=content
        )

    form.save()
    return api_response(code=http_codes.CREATED, result='success', message='Level created successfully.')

@csrf_exempt
def update_level(request):
    verify_method(expected_method='PATCH', requested_method=request.method, requested_path=request.path)

    content = json.loads(request.body.decode('utf-8'))

    try:
        level = Level.objects.get(pk=content['id'])
        if not level:
            return api_response(code=http_codes.NOT_FOUND, result='error', message='Level not found.', url=request.path)
    except Level.DoesNotExist:
        return api_response(code=http_codes.NOT_FOUND, result='error', message='Level not found.', url=request.path)

    form = LevelForm(instance=level, data=content)
    if not form.is_valid():
        return api_response(
            code=http_codes.INTERNAL_SERVER_ERROR,
            result='error',
            message='Invalid form.',
            data=form.errors,
            url=request.path,
            payload=content
        )

    form.save()
    return api_response(code=http_codes.SUCCESS, result='success', message='Level updated successfully.')


@csrf_exempt
def delete_level(request, level_id):
    verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)

    try:
        level = Level.objects.get(pk=level_id)

        if not level:
            return api_response(code=http_codes.NOT_FOUND, result='error', message='Level not found.', url=request.path)
    except Level.DoesNotExist:
        return api_response(code=http_codes.NOT_FOUND, result='error', message='Level not found.', url=request.path)

    level.is_activate = False
    level.save()
    return api_response(code=http_codes.SUCCESS, result='success', message='Level deleted successfully.')
