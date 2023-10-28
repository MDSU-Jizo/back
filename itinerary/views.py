import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime

from itinerary_type.forms import ItineraryTypeForm
from service.verify_method import verify_method
from service.OpenAi.open_ai import prepare_prompt
from service.api_response import send_json_response as api_response
from contract.constants import Constants
from .models import Itinerary, get_itineraries_with_types_and_interests, get_itinerary_with_types_and_interests
from .forms import ItineraryForm
from .normalizers import itineraries_normalizer, itinerary_normalizer
from itinerary_interest.forms import ItineraryInterestForm
from .mockups import MockUps

HttpCode = Constants.HttpResponseCodes
Types = Constants.Types


# TODO: Get Itineraries for current user


def get_period_delta(start_date, end_date) -> int or False:
    """
        Function to return the period as the delta between start date and end date

        Args:
            start_date (str): "%Y-%m-%d" format
            end_date (str): "%Y-%m-%d" format
        Returns:
            period (int)
            or
            False: if delta is negative
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    period = end - start

    if period.days < 0 :
        return False

    return period.days


def link_interests_to_itinerary(request, interests, itinerary) -> True or JsonResponse:
    """
        Function to define interests in the given itinerary

        Args:
            request (request)
            interests (list): list of interest's int
            itinerary (Itinerary)

        Returns:
            True: Valid form
            or
            JsonResponse: Invalid form
    """
    for interest in interests:
        data = {
            'itinerary': itinerary,
            'interest': interest
        }

        itinerary_interest_form = ItineraryInterestForm(data)

        if not itinerary_interest_form.is_valid():
            return api_response(
                code=HttpCode.INTERNAL_SERVER_ERROR,
                result='error',
                message='Invalid form.',
                data=itinerary_interest_form.errors,
                url=request.path,
                payload=interests
            )

        itinerary_interest_form.save()

    return True


def link_types_to_itinerary(request, types, itinerary) -> True or JsonResponse:
    """
        Function to define interests in the given itinerary

        Args:
            request (request)
            types (list): List of type's int
            itinerary (Itinerary)

        Returns:
            True: Valid form
            or
            JsonResponse: Invalid form
    """
    for type in types:
        data = {
            'itinerary': itinerary,
            'type': type
        }

        itinerary_type_form = ItineraryTypeForm(data)

        if not itinerary_type_form.is_valid():
            return api_response(
                code=HttpCode.INTERNAL_SERVER_ERROR,
                result='error',
                message='Invalid form.',
                data=itinerary_type_form.errors,
                url=request.path,
                payload=types
            )

        itinerary_type_form.save()

    return True


def get_itineraries(request) -> JsonResponse:
    """
        Function to return every itinerary

        Args:
            request
        Returns:
            JsonResponse
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        itineraries = get_itineraries_with_types_and_interests()
    except Itinerary.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success')

    normalizer = itineraries_normalizer(itineraries)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


def get_itinerary(request, itinerary_id):
    """
        Function to return a single itinerary

        Args:
            request
            itinerary_id (int)
        Returns:
            JsonResponse
    """
    has_method = verify_method(expected_method='GET', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        itinerary = get_itinerary_with_types_and_interests(itinerary_id)

        if not itinerary:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Itinerary not found.',
                url=request.path
            )
    except Itinerary.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Itinerary not found.', url=request.path)

    normalizer = itinerary_normalizer(itinerary)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


@csrf_exempt
def create_itinerary(request) -> JsonResponse:
    """
        Function to create an itinerary

        Args:
            request
        Requires:
            body: JSON
        Returns:
            JsonResponse
    """
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
    form = ItineraryForm(content)

    if not form.is_valid():
        return api_response(
            code=HttpCode.INTERNAL_SERVER_ERROR,
            result='error',
            message='Invalid form.',
            data=form.errors,
            url=request.path,
            payload=content
        )

    itinerary = form.save()

    if "interests" not in content:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Body must possess interests.',
            url=request.path,
            payload=content
        )

    interests = link_interests_to_itinerary(request, content['interests'], itinerary.id)

    if interests is not True:
        return interests

    if "types" not in content:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Body must possess types.',
            url=request.path,
            payload=content
        )

    for trip_type in content['types']:
        if (trip_type in [Types.ROADTRIP.value, Types.BACKPACKING.value, Types.HIKING.value]
                and "level" not in content):
            return api_response(
                code=HttpCode.BAD_REQUEST,
                result='error',
                message='Body must possess level for that travel type.',
                url=request.path,
                payload=content
            )

    types = link_types_to_itinerary(request, content['types'], itinerary.id)

    if types is not True:
        return types

    period = get_period_delta(content['start_date'], content['end_date'])

    if isinstance(period, bool):
        return api_response(
            code=HttpCode.NOT_ALLOWED,
            result='error',
            message='The delta between start date and end date can not be negative.',
            data={
                'start': content['start_date'],
                'end': content['end_date'],
            },
            url=request.path,
            payload=content
        )

    content['period'] = period

    if request.GET.get('test'):
        itinerary.response = MockUps.openai_response
        itinerary.save()

        return api_response(
            code=HttpCode.CREATED,
            result='success',
            message='Itinerary created successfully.',
            data=MockUps.openai_response
        )

    response = prepare_prompt(user_inputs=content)

    if not response.choices[0].text:
        return api_response(
            code=HttpCode.INTERNAL_SERVER_ERROR,
            result='error',
            message='Could not create an itinerary, retry later.',
            data=content
        )

    itinerary.response = json.loads(response.choices[0].text)

    return api_response(
        code=HttpCode.CREATED,
        result='success',
        message='Itinerary created successfully.',
        data=json.loads(response.choices[0].text)
    )


@csrf_exempt
def update_itinerary_title(request, itinerary_id) -> JsonResponse:
    """
        Function to update the title of an itinerary

        Args:
            request
            itinerary_id (int)
        Returns:
            JsonResponse
    """
    has_method = verify_method(expected_method='PATCH', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method

    try:
        itinerary = Itinerary.objects.get(pk=itinerary_id)

        if not itinerary:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Itinerary not found.',
                url=request.path
            )
    except Itinerary.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Itinerary not found.',
            url=request.path
        )

    if not request.body or json.loads(request.body) == {}:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Require a payload.',
            url=request.path,
        )

    content = json.loads(request.body.decode('utf-8'))

    if "title" not in content:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Payload requires title.',
            url=request.path
        )

    itinerary.title = content['title']
    itinerary.save()

    itineraries = get_itineraries_with_types_and_interests()
    normalizer = itineraries_normalizer(itineraries)

    return api_response(
        code=HttpCode.SUCCESS,
        result='success',
        message='Title updated successfully.',
        data=normalizer
    )


@csrf_exempt
def update_itinerary_steps(request) -> JsonResponse:
    """
        Function to update an itinerary steps

        Args:
            request
        Requires:
            body: JSON
        Returns:
            JsonResponse
    """
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
    if "id" not in content or "response" not in content:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Payload requires title.',
            url=request.path
        )

    try:
        itinerary = Itinerary.objects.get(pk=content['id'])

        if not itinerary:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Itinerary not found.',
                url=request.path
            )
    except Itinerary.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Itinerary not found.',
            url=request.path
        )

    itinerary.response = content['response']
    itinerary.save()

    updated_itinerary = get_itinerary_with_types_and_interests(itinerary.id)

    normalizer = itinerary_normalizer(updated_itinerary)

    return api_response(
        code=HttpCode.SUCCESS,
        result='success',
        message='JSON updated successfully.',
        data=normalizer
    )


@csrf_exempt
def delete_itinerary(request, itinerary_id) -> JsonResponse:
    """
        Function to delete an itinerary

        Args:
            request
            itinerary_id (int)
        Returns:
            JsonResponse
    """
    has_method = verify_method(expected_method='DELETE', requested_method=request.method, requested_path=request.path)
    if isinstance(has_method, JsonResponse):
        return has_method
    try:
        itinerary = Itinerary.objects.get(pk=itinerary_id)

        if not itinerary:
            return api_response(
                code=HttpCode.NOT_FOUND,
                result='error',
                message='Itinerary not found.',
                url=request.path
            )
    except Itinerary.DoesNotExist:
        return api_response(
            code=HttpCode.NOT_FOUND,
            result='error',
            message='Itinerary not found.',
            url=request.path
        )

    itinerary.delete()

    try:
        itineraries = get_itineraries_with_types_and_interests()
    except Itinerary.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success')

    normalizer = itineraries_normalizer(itineraries)
    return api_response(
        HttpCode.SUCCESS,
        result='success',
        message='Itinerary delete successfully.',
        data=normalizer
    )
