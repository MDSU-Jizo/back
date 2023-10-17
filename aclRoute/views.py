"""
    AclRoute views
"""
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import AclRoute, get_acl_routes_with_bundles, get_acl_route_with_bundles
from .normalizers import acl_routes_normalizer, acl_route_normalizer
from .forms import AclRouteForm
from service.api_response import send_json_response as api_response
from service.verify_method import verify_method
from contract.constants import Constants

HttpCode = Constants.HttpResponseCodes


@csrf_exempt
def get_acl_routes(request):
    """
        Function to fetch every acl_route from database

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
        acl_routes = get_acl_routes_with_bundles(filter)
    except AclRoute.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success')

    normalizer = acl_routes_normalizer(acl_routes)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


@csrf_exempt
def get_acl_route(request, acl_route_id):
    """
        Function to fetch every acl_route from database

        Args:
            request: Request header containing authorization and method
            acl_route_id (int): id of the acl_route
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        acl_route = get_acl_route_with_bundles(acl_route_id)

        if not acl_route:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='AclRoute not found.', url=request.path)
    except AclRoute.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='AclRoute not found.', url=request.path)

    normalizer = acl_route_normalizer(acl_route)
    return api_response(code=HttpCode.SUCCESS, result='success', data=normalizer)


@csrf_exempt
def add_acl_route(request):
    """
        Function to add a acl_route in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    content = json.loads(request.body.decode('utf-8'))
    form = AclRouteForm(content)
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
    return api_response(code=HttpCode.CREATED, result='success', message='AclRoute created successfully.')


@csrf_exempt
def update_acl_route(request):
    """
        Function to update a acl_route in database

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
        acl_route = AclRoute.objects.get(pk=content['id'])
        if not acl_route:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='AclRoute not found.',
                url=request.path,
                payload=content
            )
    except AclRoute.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='AclRoute not found.',
            url=request.path,
            payload=content
        )

    form = AclRouteForm(instance=acl_route, data=content)
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
    return api_response(code=HttpCode.SUCCESS, result='success', message='AclRoute updated successfully.')


@csrf_exempt
def delete_acl_route(request, acl_route_id):
    """
        Function to set is_active to False on a acl_route in database

        Args:
            request: Request header containing authorization and method
            acl_route_id: id of the acl_route
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        acl_route = AclRoute.objects.get(pk=acl_route_id)

        if not acl_route:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='AclRoute not found.', url=request.path)
    except AclRoute.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='AclRoute not found.', url=request.path)

    acl_route.is_activate = False
    acl_route.save()
    return api_response(code=HttpCode.SUCCESS, result='success', message='AclRoute deleted successfully.')
