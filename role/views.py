"""
    Role views
"""
import json

from django.http import JsonResponse
from .models import Role
from .normalizers import roles_normalizer, role_normalizer
from .forms import RoleForm
from service.api_response import send_json_response as api_response
from service.verify_method import verify_method
from contract.constants import Constants

HttpCode = Constants.HttpResponseCodes


def get_roles(request):
    """
        Function to fetch every role from database

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
        roles = Role.objects.all().values().filter(is_activate=filter)
    except Role.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success')

    normalizer = roles_normalizer(roles)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


def get_role(request, role_id):
    """
        Function to fetch every role from database

        Args:
            request: Request header containing authorization and method
            role_id (int): id of the role
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        role = Role.objects.get(pk=role_id)

        if not role:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Role not found.', url=request.path)
    except Role.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Role not found.', url=request.path)

    normalizer = role_normalizer(role)
    return api_response(code=HttpCode.SUCCESS, result='success', data=normalizer)


def add_role(request):
    """
        Function to add a role in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    content = json.loads(request.body.decode('utf-8'))
    form = RoleForm(content)
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
    return api_response(code=HttpCode.CREATED, result='success', message='Role created successfully.')


def update_role(request):
    """
        Function to update a role in database

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
        role = Role.objects.get(pk=content['id'])
        if not role:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Role not found.',
                url=request.path,
                payload=content
            )
    except Role.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Role not found.',
            url=request.path,
            payload=content
        )

    form = RoleForm(instance=role, data=content)
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
    return api_response(code=HttpCode.SUCCESS, result='success', message='Role updated successfully.')


def delete_role(request, role_id):
    """
        Function to set is_active to False on a role in database

        Args:
            request: Request header containing authorization and method
            role_id: id of the role
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        role = Role.objects.get(pk=role_id)

        if not role:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Role not found.', url=request.path)
    except Role.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Role not found.', url=request.path)

    role.is_activate = False
    role.save()
    return api_response(code=HttpCode.SUCCESS, result='success', message='Role deleted successfully.')
