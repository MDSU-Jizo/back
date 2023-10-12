"""
    AclBundle views
"""
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import AclBundle, get_acl_bundles_with_routes, get_acl_bundle_with_routes
from .normalizers import acl_bundles_normalizer, acl_bundle_normalizer
from .forms import AclBundleForm
from service.api_response import send_json_response as api_response
from service.verify_method import verify_method
from contract.constants import Constants

HttpCode = Constants.HttpResponseCodes


@csrf_exempt
def get_acl_bundles(request):
    """
        Function to fetch every acl_bundle from database

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
        acl_bundles = get_acl_bundles_with_routes(filter)
    except AclBundle.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success', data=[])

    normalizer = acl_bundles_normalizer(acl_bundles)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


@csrf_exempt
def get_acl_bundle(request, acl_bundle_id):
    """
        Function to fetch every acl_bundle from database

        Args:
            request: Request header containing authorization and method
            acl_bundle_id (int): id of the acl_bundle
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        acl_bundle = get_acl_bundle_with_routes(acl_bundle_id)

        if not acl_bundle:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='AclBundle not found.', url=request.path)
    except AclBundle.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='AclBundle not found.', url=request.path)

    normalizer = acl_bundle_normalizer(acl_bundle)
    return api_response(code=HttpCode.SUCCESS, result='success', data=normalizer)


@csrf_exempt
def add_acl_bundle(request):
    """
        Function to add a acl_bundle in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    content = json.loads(request.body.decode('utf-8'))
    form = AclBundleForm(content)
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
    return api_response(code=HttpCode.CREATED, result='success', message='AclBundle created successfully.')


@csrf_exempt
def update_acl_bundle(request):
    """
        Function to update a acl_bundle in database

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
        acl_bundle = AclBundle.objects.get(pk=content['id'])
        if not acl_bundle:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='AclBundle not found.',
                url=request.path,
                payload=content
            )
    except AclBundle.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='AclBundle not found.',
            url=request.path,
            payload=content
        )

    form = AclBundleForm(instance=acl_bundle, data=content)
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
    return api_response(code=HttpCode.SUCCESS, result='success', message='AclBundle updated successfully.')


@csrf_exempt
def delete_acl_bundle(request, acl_bundle_id):
    """
        Function to set is_active to False on a acl_bundle in database

        Args:
            request: Request header containing authorization and method
            acl_bundle_id: id of the acl_bundle
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        acl_bundle = AclBundle.objects.get(pk=acl_bundle_id)

        if not acl_bundle:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='AclBundle not found.', url=request.path)
    except AclBundle.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='AclBundle not found.', url=request.path)

    acl_bundle.is_activate = False
    acl_bundle.save()
    return api_response(code=HttpCode.SUCCESS, result='success', message='AclBundle deleted successfully.')
