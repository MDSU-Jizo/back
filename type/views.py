"""
    Type views
"""
import json

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Type
from .normalizers import types_normalizer, type_normalizer
from .forms import TypeForm
from service.api_response import send_json_response as api_response
from service.verify_method import verify_method
from contract.constants import Constants

HttpCode = Constants.HttpResponseCodes


def get_types(request):
    """
        Function to fetch every type from database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
        Filter:
            isActivate (False, optional with default value to True): Fetched from request url parameter.
    """
    verify_method('GET', request.method, requested_path=request.path)

    filter = request.GET.get('isActivate', True)
    try:
        types = Type.objects.all().values().filter(is_activate=filter)
    except Type.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success', data=[])

    normalizer = types_normalizer(types)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


def get_type(request, type_id):
    """
        Function to fetch every type from database

        Args:
            request: Request header containing authorization and method
            type_id (int): id of the type
        Returns:
            JsonResponse containing request's information
    """
    verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)

    try:
        type = Type.objects.get(pk=type_id)

        if not type:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Type not found.', url=request.path)
    except Type.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Type not found.', url=request.path)

    normalizer = type_normalizer(type)
    return api_response(code=HttpCode.SUCCESS, result='success', data=normalizer)

@csrf_exempt
def add_type(request):
    """
        Function to add a type in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)

    content = json.loads(request.body.decode('utf-8'))
    form = TypeForm(content)
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
    return api_response(code=HttpCode.CREATED, result='success', message='Type created successfully.')

@csrf_exempt
def update_type(request):
    """
        Function to update a type in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    verify_method(expected_method='PATCH', requested_method=request.method, requested_path=request.path)

    content = json.loads(request.body.decode('utf-8'))

    try:
        type = Type.objects.get(pk=content['id'])
        if not type:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Type not found.',
                url=request.path,
                payload=content
            )
    except Type.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Type not found.',
            url=request.path,
            payload=content
        )

    form = TypeForm(instance=type, data=content)
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
    return api_response(code=HttpCode.SUCCESS, result='success', message='Type updated successfully.')


@csrf_exempt
def delete_type(request, type_id):
    """
        Function to set is_active to False on a type in database

        Args:
            request: Request header containing authorization and method
            type_id: id of the type
        Returns:
            JsonResponse containing request's information
    """
    verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)

    try:
        type = Type.objects.get(pk=type_id)

        if not type:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Type not found.', url=request.path)
    except Type.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Type not found.', url=request.path)

    type.is_activate = False
    type.save()
    return api_response(code=HttpCode.SUCCESS, result='success', message='Type deleted successfully.')
