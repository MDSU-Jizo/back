"""
    Interest views
"""
import json

from django.http import JsonResponse
from .models import Interest
from .normalizers import interests_normalizer, interest_normalizer
from .forms import InterestForm
from service.api_response import send_json_response as api_response
from service.verify_method import verify_method
from contract.constants import Constants

HttpCode = Constants.HttpResponseCodes


def get_interests(request):
    """
        Function to fetch every interest from database

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
        interests = Interest.objects.all().values().filter(is_activate=filter)
    except Interest.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success')

    normalizer = interests_normalizer(interests)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


def get_interest(request, interest_id):
    """
        Function to fetch every interest from database

        Args:
            request: Request header containing authorization and method
            interest_id (int): id of the interest
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        interest = Interest.objects.get(pk=interest_id)

        if not interest:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Interest not found.', url=request.path)
    except Interest.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Interest not found.', url=request.path)

    normalizer = interest_normalizer(interest)
    return api_response(code=HttpCode.SUCCESS, result='success', data=normalizer)


def add_interest(request):
    """
        Function to add a interest in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    content = json.loads(request.body.decode('utf-8'))
    form = InterestForm(content)
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
    return api_response(code=HttpCode.CREATED, result='success', message='Interest created successfully.')


def update_interest(request):
    """
        Function to update a interest in database

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
        interest = Interest.objects.get(pk=content['id'])
        if not interest:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Interest not found.',
                url=request.path,
                payload=content
            )
    except Interest.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Interest not found.',
            url=request.path,
            payload=content
        )

    form = InterestForm(instance=interest, data=content)
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
    return api_response(code=HttpCode.SUCCESS, result='success', message='Interest updated successfully.')


def delete_interest(request, interest_id):
    """
        Function to set is_active to False on a interest in database

        Args:
            request: Request header containing authorization and method
            interest_id: id of the interest
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        interest = Interest.objects.get(pk=interest_id)

        if not interest:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Interest not found.', url=request.path)
    except Interest.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Interest not found.', url=request.path)

    interest.is_activate = False
    interest.save()
    return api_response(code=HttpCode.SUCCESS, result='success', message='Interest deleted successfully.')
