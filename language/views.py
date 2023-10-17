"""
    Language views
"""
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Language
from .normalizers import languages_normalizer, language_normalizer
from .forms import LanguageForm
from service.api_response import send_json_response as api_response
from service.verify_method import verify_method
from contract.constants import Constants

HttpCode = Constants.HttpResponseCodes


@csrf_exempt
def get_languages(request):
    """
        Function to fetch every language from database

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
        languages = Language.objects.all().values().filter(is_activate=filter)
    except Language.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success')

    normalizer = languages_normalizer(languages)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


@csrf_exempt
def get_language(request, language_id):
    """
        Function to fetch every language from database

        Args:
            request: Request header containing authorization and method
            language_id (int): id of the language
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        language = Language.objects.get(pk=language_id)

        if not language:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Language not found.', url=request.path)
    except Language.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Language not found.', url=request.path)

    normalizer = language_normalizer(language)
    return api_response(code=HttpCode.SUCCESS, result='success', data=normalizer)


@csrf_exempt
def add_language(request):
    """
        Function to add a language in database

        Args:
            request: Request header containing authorization and method
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='POST', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    content = json.loads(request.body.decode('utf-8'))
    form = LanguageForm(content)
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
    return api_response(code=HttpCode.CREATED, result='success', message='Language created successfully.')


@csrf_exempt
def update_language(request):
    """
        Function to update a language in database

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
        language = Language.objects.get(pk=content['id'])
        if not language:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Language not found.',
                url=request.path,
                payload=content
            )
    except Language.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Language not found.',
            url=request.path,
            payload=content
        )

    form = LanguageForm(instance=language, data=content)
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
    return api_response(code=HttpCode.SUCCESS, result='success', message='Language updated successfully.')


@csrf_exempt
def delete_language(request, language_id):
    """
        Function to set is_active to False on a language in database

        Args:
            request: Request header containing authorization and method
            language_id: id of the language
        Returns:
            JsonResponse containing request's information
    """
    has_method = verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        language = Language.objects.get(pk=language_id)

        if not language:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Language not found.', url=request.path)
    except Language.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Language not found.', url=request.path)

    language.is_activate = False
    language.save()
    return api_response(code=HttpCode.SUCCESS, result='success', message='Language deleted successfully.')
