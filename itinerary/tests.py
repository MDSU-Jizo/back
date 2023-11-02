"""
    Itinerary Unit Tests
"""
import json

from django.http import JsonResponse
from django.test import TestCase, RequestFactory

from user.views import encode_user_as_jwt
from .models import Itinerary
from .views import (
    get_period_delta,
    get_itineraries,
    get_itinerary,
    link_interests_to_itinerary,
    link_types_to_itinerary,
    create_itinerary,
    update_itinerary_title,
    update_itinerary_steps,
    delete_itinerary
)
from interest.models import Interest
from type.models import Type
from user.models import User
from language.models import Language
from role.models import Role
from level.models import Level
from .mockups import MockUps


class ItineraryTestCase(TestCase):
    """
        Test cases for Itinerary API
    """
    def setUp(self):
        self.maxDiff = None
        self.factory = RequestFactory()
        self.language = Language.objects.create(id=1, label="French")
        self.role = Role.objects.create(id=1, label="ROLE_USER")
        self.user = User.objects.create(
            id=1,
            firstname="Axel",
            lastname="Pion",
            email="test.case@gmail.com",
            birthdate="1992-10-18",
            gender=1,
            country="France",
            language=self.language,
            role=self.role
        )
        self.interest_monument = Interest.objects.create(id=1, label="Monument")
        self.interest_gastronomy = Interest.objects.create(id=2, label="Gastronomy")
        self.interest_nature = Interest.objects.create(id=3, label="Nature")
        self.type_tourism = Type.objects.create(id=1, label="Tourism")
        self.type_hiking = Type.objects.create(id=2, label="Hiking")
        self.level_beginner = Level.objects.create(id=1, label="Beginner")
        self.level_intermediate = Level.objects.create(id=2, label="Intermediate")
        self.level_experimented = Level.objects.create(id=3, label="Experimented")
        self.interests = [1, 2, 3]
        self.bad_interests = ["Gastronomy"]
        self.types = [1]
        self.bad_types = ["Tourism"]
        self.response = MockUps.response
        self.itinerary = Itinerary.objects.create(
            id=333,
            title="France",
            country="France",
            starting_city="Paris",
            start_date="2023-12-20",
            end_date="2023-12-27",
            multiple_cities=False,
            user=self.user,
            response=self.response
        )
        self.max_number_of_steps = 3
        self.max_number_of_activities = 4

    def test_link_interests_to_itinerary(self):
        request = self.factory.post("/itinerary/create")
        response = link_interests_to_itinerary(request, self.interests, self.itinerary)

        self.assertEqual(response, True)

    def test_wrong_link_interests_to_itinerary(self):
        request = self.factory.post("/itinerary/create")
        response = link_interests_to_itinerary(request, self.bad_interests, self.itinerary)

        self.assertEqual(type(response), JsonResponse)
        self.assertJSONEqual(response.content, MockUps.wrong_interests_response)

    def test_link_types_to_itinerary(self):
        request = self.factory.post("/itinerary/create")
        response = link_types_to_itinerary(request, self.types, self.itinerary)

        self.assertEqual(response, True)

    def test_wrong_link_types_to_itinerary(self):
        request = self.factory.post("/itinerary/create")
        response = link_interests_to_itinerary(request, self.bad_types, self.itinerary)

        self.assertEqual(type(response), JsonResponse)
        self.assertJSONEqual(response.content, MockUps.wrong_types_response)

    def test_get_itineraries(self):
        request = self.factory.get("/itinerary")
        response = get_itineraries(request)
        itineraries = json.loads(response.content)

        for itinerary in itineraries['data']:
            del itinerary['created_at']
            del itinerary['updated_at']

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(json.dumps(itineraries), MockUps.itineraries_response)

    def test_get_itineraries_bad_methods(self):
        request = self.factory.post("/itinerary")
        response = get_itineraries(request)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_get_response)

    def test_get_itinerary(self):
        id = 333
        request = self.factory.get(f"/itinerary/details/{id}")
        response = get_itinerary(request, id)
        itinerary = json.loads(response.content)

        del itinerary['data']['created_at']
        del itinerary['data']['updated_at']

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(json.dumps(itinerary), MockUps.itinerary_response)

    def test_get_itinerary_not_found(self):
        id = 999
        request = self.factory.get(f"/itinerary/details/{id}")
        response = get_itinerary(request, id)

        self.assertJSONEqual(response.content, MockUps.itinerary_not_found_response)

    def test_get_itinerary_bad_method(self):
        id = 999
        request = self.factory.post(f"/itinerary/details/{id}")
        response = get_itinerary(request, id)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_get_response)

    def test_create_itinerary(self):
        request = self.factory.post(
            "/itinerary/create?test=True",
            data=MockUps.create_itinerary_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = create_itinerary(request)

        self.assertJSONEqual(response.content, MockUps.create_itinerary_response)

    def test_create_itinerary_bad_method(self):
        request = self.factory.get('itinerary/create?test=True')
        response = create_itinerary(request)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_post_response)

    def test_create_itinerary_without_payload(self):
        request = self.factory.post("/itinerary/create?test=True", content_type='application/json')
        response = create_itinerary(request)

        self.assertJSONEqual(response.content, MockUps.create_itinerary_without_payload_response)

    def test_create_itinerary_bad_payload(self):
        request = self.factory.post(
            "/itinerary/create?test=True",
            data=MockUps.create_itinerary_bad_payload,
            content_type='application/json'
        )
        response = create_itinerary(request)

        self.assertJSONEqual(response.content, MockUps.create_itinerary_bad_payload_response)

    def test_create_itinerary_payload_without_types(self):
        request = self.factory.post(
            "/itinerary/create?test=True",
            data=MockUps.create_itinerary_without_types_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = create_itinerary(request)

        self.assertJSONEqual(response.content, MockUps.create_itinerary_without_types_response)

    def test_create_itinerary_payload_without_interests(self):
        request = self.factory.post(
            "/itinerary/create?test=True",
            data=MockUps.create_itinerary_without_interests_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = create_itinerary(request)

        self.assertJSONEqual(response.content, MockUps.create_itinerary_without_interests_response)

    def test_create_itinerary_payload_with_bad_delta(self):
        request = self.factory.post(
            "/itinerary/create?test=True",
            data=MockUps.create_itinerary_bad_delta_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = create_itinerary(request)

        self.assertJSONEqual(response.content, MockUps.create_itinerary_bad_delta_response)

    def test_update_itinerary_title(self):
        id = 333
        request = self.factory.patch(
            f"/itinerary/update/{id}",
            data=MockUps.update_itinerary_title_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = update_itinerary_title(request, id)
        itineraries = json.loads(response.content)

        for itinerary in itineraries['data']:
            del itinerary['created_at']
            del itinerary['updated_at']

        self.assertJSONEqual(json.dumps(itineraries), MockUps.update_itinerary_title_response)

    def test_update_itinerary_title_with_bad_method(self):
        id = 333
        request = self.factory.get(
            f"/itinerary/update/{id}",
            data=MockUps.update_itinerary_title_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = update_itinerary_title(request, id)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_patch_response)

    def test_update_itinerary_title_as_int_type(self):
        id = 333
        request = self.factory.patch(
            f"/itinerary/update/{id}",
            data=MockUps.update_itinerary_title_as_int_type_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = update_itinerary_title(request, id)
        itineraries = json.loads(response.content)

        for itinerary in itineraries['data']:
            del itinerary['created_at']
            del itinerary['updated_at']

        self.assertJSONEqual(json.dumps(itineraries), MockUps.update_itinerary_title_as_int_type_response)

    def test_update_itinerary_title_on_itinerary_not_found(self):
        id = 777
        request = self.factory.patch(
            f"/itinerary/update/{id}",
            data=MockUps.update_itinerary_title_as_int_type_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = update_itinerary_title(request, id)

        self.assertJSONEqual(response.content, MockUps.itinerary_not_found_response)

    def test_update_itinerary_steps(self):
        request = self.factory.patch(
            f"/itinerary/update",
            data=MockUps.update_itinerary_steps_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = update_itinerary_steps(request)
        itinerary = json.loads(response.content)

        del itinerary['data']['created_at']
        del itinerary['data']['updated_at']

        self.assertJSONEqual(json.dumps(itinerary), MockUps.update_itinerary_steps_response)

    def test_update_itinerary_steps_with_bad_method(self):
        request = self.factory.get(
            f"/itinerary/update",
            data=MockUps.update_itinerary_steps_payload,
            content_type='application/json'
        )
        response = update_itinerary_steps(request)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_patch_response)

    def test_update_itinerary_steps_on_itinerary_not_found(self):
        request = self.factory.patch(
            f"/itinerary/update",
            data=MockUps.update_itinerary_steps_on_itinerary_not_found_payload,
            content_type='application/json'
        )
        request.user_id = self.user.id
        response = update_itinerary_steps(request)

        self.assertJSONEqual(response.content, MockUps.itinerary_not_found_response)