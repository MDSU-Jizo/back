import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime

from service.verify_method import verify_method
from service.OpenAi.open_ai import prepare_prompt
from service.api_response import send_json_response as api_response
from contract.constants import Constants
from .models import Itinerary
from .forms import ItineraryForm
from .normalizers import itineraries_normalizer, itinerary_normalizer
from itinerary_interest.forms import ItineraryInterestForm

HttpCode = Constants.HttpResponseCodes

TEST_JSON = """
{
    "country": "France",
    "itinerary": [
        {
            "city": "Paris",
            "duration": 2,
            "todo": [
                {
                    "name": "Eiffel Tower",
                    "longitude": "2.2945",
                    "latitude": "48.8584",
                    "category": "Monument"
                },
                {
                    "name": "Louvre Museum",
                    "longitude": "2.3387",
                    "latitude": "48.8606",
                    "category": "Monument"
                },
                {
                    "name": "Le Petit Cler",
                    "longitude": "2.3387",
                    "latitude": "48.8617",
                    "category": "Gastronomy"
                },
                {
                    "name": "Jardin des Tuileries",
                    "longitude": "2.3317",
                    "latitude": "48.8637",
                    "category": "Nature"
                }
            ]
        },
        {
            "city": "Nice",
            "duration": 2,
            "todo": [
                {
                    "name": "Promenade des Anglais",
                    "longitude": "7.2662",
                    "latitude": "43.6961",
                    "category": "Discovering"
                },
                {
                    "name": "Vieux Nice",
                    "longitude": "7.2710",
                    "latitude": "43.6984",
                    "category": "Discovering"
                },
                {
                    "name": "Chez Pipo",
                    "longitude": "7.2710",
                    "latitude": "43.6984",
                    "category": "Gastronomy"
                },
                {
                    "name": "Parc Phoenix",
                    "longitude": "7.2662",
                    "latitude": "43.6961",
                    "category": "Nature"
                }
            ]
        },
        {
            "city": "Paris",
            "duration": 2,
            "todo": [
                {
                    "name": "Notre Dame Cathedral",
                    "longitude": "2.3470",
                    "latitude": "48.8530",
                    "category": "Monument"
                },
                {
                    "name": "Arc de Triomphe",
                    "longitude": "2.2950",
                    "latitude": "48.8738",
                    "category": "Monument"
                },
                {
                    "name": "Le Petit Cler",
                    "longitude": "2.3387",
                    "latitude": "48.8617",
                    "category": "Gastronomy"
                },
                {
                    "name": "Jardin des Tuileries",
                    "longitude": "2.3317",
                    "latitude": "48.8637",
                    "category": "Nature"
                }
            ]
        }
    ]
}
"""

# TODO: Get Itineraries for current user


def get_period_delta(start_date, end_date) -> int | False:
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

    if period.days < 0:
        return False

    return period


def link_interests_to_itinerary(request, interests, itinerary) -> True | JsonResponse:
    """
        Function to define interests in the given itinerary

        Args:
            request (request)
            interests (dict): Dict of interest's int
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
        itineraries = Itinerary.objects.all().values()
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
        itinerary = Itinerary.objects.get(pk=itinerary_id)

        if not itinerary:
            return api_response(code=HttpCode.NOT_FOUND, result='error', message='Itinerary not found.',
                                url=request.path)
    except Itinerary.DoesNotExist:
        return api_response(code=HttpCode.NOT_FOUND, result='error', message='Itinerary not found.', url=request.path)

    normalizer = itinerary_normalizer(itinerary)
    return api_response(HttpCode.SUCCESS, 'success', data=normalizer)


@csrf_exempt
def create_itinerary(request):
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

    if not request.body:
        return api_response(
            code=HttpCode.FORBIDDEN,
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

    if content['interests']:
        interests = link_interests_to_itinerary(request, content['interests'], itinerary.id)

        if interests is not True:
            return interests

    period = get_period_delta(content['start_date'], content['end_date'])

    if not period:
        return api_response(
            code=HttpCode.NOT_ALLOWED,
            result='error',
            message='The delta between start date and end date can not be negative.',
            data={
                'start': content['start_date'],
                'end': content['end_date'],
                'delta': period.days
            },
            url=request.path,
            payload=content
        )

    content['period'] = period

    response = prepare_prompt(user_inputs=content)

    if not response.choices[0].text:
        return api_response(
            code=HttpCode.INTERNAL_SERVER_ERROR,
            result='error',
            message='Could not create an itinerary, retry later.',
            data=content
        )

    itinerary.response = json.loads(response.choices[0].text)
    # itinerary.response = json.loads(TEST_JSON)
    itinerary.save()

    return api_response(
        code=HttpCode.CREATED,
        result='success',
        message='Itinerary created successfully.',
        data=json.loads(response.choices[0].text)
    )

    # return api_response(
    #     code=HttpCode.CREATED,
    #     result='success',
    #     message='Itinerary created successfully.',
    #     data=json.loads(TEST_JSON)
    # )


@csrf_exempt
def update_itinerary_title(request, itinerary_id):
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

    content = json.loads(request.body.decode('utf-8'))

    if not content['title']:
        return api_response(
            code=HttpCode.BAD_REQUEST,
            result='error',
            message='Payload requires title.',
            url=request.path
        )

    itinerary.title = content['title']
    itinerary.save()

    itineraries = Itinerary.objects.all().values()
    normalizer = itineraries_normalizer(itineraries)

    return api_response(
        code=HttpCode.SUCCESS,
        result='success',
        message='Title updated successfully.',
        data=normalizer
    )


@csrf_exempt
def update_itinerary_steps(request):
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

    content = json.loads(request.body.decode('utf-8'))
    if not content['id'] or not content['response']:
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

    normalizer = itinerary_normalizer(itinerary)

    return api_response(
        code=HttpCode.SUCCESS,
        result='success',
        message='JSON updated successfully.',
        data=normalizer
    )


@csrf_exempt
def delete_itinerary(request, itinerary_id):
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
        itineraries = Itinerary.objects.all().values()
    except Itinerary.DoesNotExist:
        return api_response(HttpCode.SUCCESS, 'success')

    normalizer = itineraries_normalizer(itineraries)
    return api_response(
        HttpCode.SUCCESS,
        result='success',
        message='Itinerary delete successfully.',
        data=normalizer
    )
