"""
    Interest Unit Tests
"""
from django.test import TestCase, RequestFactory
from .models import Interest
from .views import get_interests, get_interest, add_interest, update_interest, delete_interest


class InterestTestCase(TestCase):
    """
        Test cases for Interest API
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.interest = Interest.objects.create(id=2, label="UnitTestInterest")
        self.activated_interests_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestInterest",
                    "isActivate": True
                }
            ]
        }
        self.empty_interest_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": []
        }
        self.deactivated_interests_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestInterest",
                    "isActivate": False
                }
            ]
        }
        self.interest_details_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": {
                "id": 2,
                "label": "UnitTestInterest"
            }
        }
        self.interest_not_found_response = {
            "code": 404,
            "result": "error",
            "message": "Interest not found.",
            "data": []
        }
        self.interest_deleted_response = {
            "code": 200,
            "result": "success",
            "message": "Interest deleted successfully.",
            "data": []
        }
        self.interest_add_payload = {
            "label": "UnitTestAddInterest"
        }
        self.interest_add_response = {
            "code": 201,
            "result": "success",
            "message": "Interest created successfully.",
            "data": []
        }
        self.interest_add_bad_payload = {
            "title": "UnitTestAddInterest"
        }
        self.interest_add_bad_payload_response = {
            "code": 500,
            "result": "error",
            "message": "Invalid form.",
            "data": {
                "label": [
                    "This field is required."
                ]
            }
        }
        self.interest_update_payload = {
            "id": 2,
            "label": "UnitTestUpdateInterest"
        }
        self.interest_update_response = {
            "code": 200,
            "result": "success",
            "message": "Interest updated successfully.",
            "data": []
        }
        self.interest_update_bad_payload = {
            "id": 2,
            "title": "UnitTestUpdateInterest"
        }
        self.interest_update_not_found = {
            "id": 666,
            "label": "UnitTestUpdateInterest"
        }
        self.interest_bad_method_on_get_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a GET method.",
            "data": []
        }
        self.interest_bad_method_on_post_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a POST method.",
            "data": []
        }
        self.interest_bad_method_on_patch_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a PATCH method.",
            "data": []
        }
        self.interest_bad_method_on_delete_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a DELETE method.",
            "data": []
        }

    def test_get_activated_interests(self):
        """
            Unit test on get_interests route without filter
        """
        request = self.factory.get("/interest/")
        response = get_interests(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.activated_interests_response)

    def test_get_empty_interests(self):
        """
            Unit test on get_interests route with filter set to False while the database has no entity set to False
        """
        request = self.factory.get("/interest/?isActivate=False")
        response = get_interests(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.empty_interest_response)

    def test_get_interest(self):
        """
            Unit test on get_interest route
        """
        id = 2
        request = self.factory.get(f"/interest/details/{id}")
        response = get_interest(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.interest_details_response)

    def test_get_interest_not_found(self):
        """
            Unit test on get_interest route with the wrong interest id
        """
        id = 666
        request = self.factory.get(f"/interest/{id}")
        response = get_interest(request, id)

        self.assertJSONEqual(response.content, self.interest_not_found_response)

    def test_delete_interest(self):
        """
            Unit test on delete_interest route to deactivate a interest
        """
        id = 2
        request = self.factory.delete(f"/interest/delete/{id}")
        response = delete_interest(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.interest_deleted_response)

    def test_delete_not_found_interest(self):
        """
            Unit test on delete_interest route with the wrong id
        """
        id = 666
        request = self.factory.delete(f"/interest/delete/{id}")
        response = delete_interest(request, id)

        self.assertJSONEqual(response.content, self.interest_not_found_response)

    def test_get_deactivated_interests(self):
        """
            Unit test on get_interests route with filter set to False
        """
        Interest.objects.update(id=2, label="UnitTestInterest", is_activate=False)
        request = self.factory.get("/interest/?isActivate=False")
        response = get_interests(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.deactivated_interests_response)

    def test_add_interest(self):
        """
            Unit test on add_interest route
        """
        request = self.factory.post("/interest/add", data=self.interest_add_payload, content_type='application/json')
        response = add_interest(request)

        self.assertJSONEqual(response.content, self.interest_add_response)

    def test_add_interest_with_bad_payload(self):
        """
            Unit test on add_interest route with bad payload
        """
        request = self.factory.post("/interest/add", data=self.interest_add_bad_payload, content_type='application/json')
        response = add_interest(request)

        self.assertJSONEqual(response.content, self.interest_add_bad_payload_response)

    def test_update_interest(self):
        """
            Unit test on update_interest route
        """
        request = self.factory.patch("/interest/update", data=self.interest_update_payload, content_type='application/json')
        response = update_interest(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.interest_update_response)

    def test_update_interest_bad_payload(self):
        """
            Unit test on update_interest route with bad payload
        """
        request = self.factory.patch("/interest/update", data=self.interest_update_bad_payload, content_type='application/json')
        response = update_interest(request)

        self.assertJSONEqual(response.content, self.interest_add_bad_payload_response)

    def test_update_interest_on_interest_not_found(self):
        """
            Unit test on update_interest route with bad id in payload
        """
        request = self.factory.patch("/interest/update", self.interest_update_not_found, content_type='application/json')
        response = update_interest(request)

        self.assertJSONEqual(response.content, self.interest_not_found_response)

    def test_get_interests_with_bad_method(self):
        """
            Unit test on get_interests route with bad request method
        """
        request = self.factory.post("/interest/")
        response = get_interests(request)

        self.assertJSONEqual(response.content, self.interest_bad_method_on_get_response)

    def test_get_interest_with_bad_method(self):
        """
            Unit test on get_interest route with bad request method
        """
        id = 2
        request = self.factory.post(f"/interest/details/{id}")
        response = get_interest(request, id)

        self.assertJSONEqual(response.content, self.interest_bad_method_on_get_response)

    def test_add_interest_with_bad_method(self):
        """
            Unit test on add_interest route with bad request method
        """
        request = self.factory.patch("/interest/add", self.interest_add_payload, content_type='application/json')
        response = add_interest(request)

        self.assertJSONEqual(response.content, self.interest_bad_method_on_post_response)

    def test_update_interest_with_bad_method(self):
        """
            Unit test on update_interest route with bad request method
        """
        request = self.factory.post("/interest/update", self.interest_update_payload, content_type='application/json')
        response = update_interest(request)

        self.assertJSONEqual(response.content, self.interest_bad_method_on_patch_response)

    def test_delete_interest_with_bad_method(self):
        """
            Unit test on delete_interest route with bad request method
        """
        id = 2
        request = self.factory.get(f"/interest/delete/{id}")
        response = delete_interest(request, id)

        self.assertJSONEqual(response.content, self.interest_bad_method_on_delete_response)