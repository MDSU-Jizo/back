"""
    Type Unit Tests
"""
from django.test import TestCase
from django.test import TestCase, RequestFactory
from .models import Type
from .views import get_types, get_type, add_type, update_type, delete_type


class TypeTestCase(TestCase):
    """
        Test cases for Type API
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.type = Type.objects.create(id=2, label="UnitTestType")
        self.activated_types_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestType",
                    "isActivate": True
                }
            ]
        }
        self.empty_type_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": []
        }
        self.deactivated_types_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestType",
                    "isActivate": False
                }
            ]
        }
        self.type_details_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": {
                "id": 2,
                "label": "UnitTestType"
            }
        }
        self.type_not_found_response = {
            "code": 404,
            "result": "error",
            "message": "Type not found.",
            "data": []
        }
        self.type_deleted_response = {
            "code": 200,
            "result": "success",
            "message": "Type deleted successfully.",
            "data": []
        }
        self.type_add_payload = {
            "label": "UnitTestAddType"
        }
        self.type_add_response = {
            "code": 201,
            "result": "success",
            "message": "Type created successfully.",
            "data": []
        }
        self.type_add_bad_payload = {
            "title": "UnitTestAddType"
        }
        self.type_add_bad_payload_response = {
            "code": 500,
            "result": "error",
            "message": "Invalid form.",
            "data": {
                "label": [
                    "This field is required."
                ]
            }
        }
        self.type_update_payload = {
            "id": 2,
            "label": "UnitTestUpdateType"
        }
        self.type_update_response = {
            "code": 200,
            "result": "success",
            "message": "Type updated successfully.",
            "data": []
        }
        self.type_update_bad_payload = {
            "id": 2,
            "title": "UnitTestUpdateType"
        }
        self.type_update_not_found_payload = {
            "id": 666,
            "label": "UnitTestUpdateType"
        }
        self.type_bad_method_on_get_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a GET method.",
            "data": []
        }
        self.type_bad_method_on_post_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a POST method.",
            "data": []
        }
        self.type_bad_method_on_patch_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a PATCH method.",
            "data": []
        }
        self.type_bad_method_on_delete_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a DELETE method.",
            "data": []
        }

    def test_get_activated_types(self):
        """
            Unit test on get_types route without filter
        """
        request = self.factory.get("/type/")
        response = get_types(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.activated_types_response)

    def test_get_empty_types(self):
        """
            Unit test on get_types route with filter set to False while the database has no entity set to False
        """
        request = self.factory.get("/type/?isActivate=False")
        response = get_types(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.empty_type_response)

    def test_get_type(self):
        """
            Unit test on get_type route
        """
        id = 2
        request = self.factory.get(f"/type/details/{id}")
        response = get_type(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.type_details_response)

    def test_get_type_not_found(self):
        """
            Unit test on get_type route with the wrong type id
        """
        id = 666
        request = self.factory.get(f"/type/{id}")
        response = get_type(request, id)

        self.assertJSONEqual(response.content, self.type_not_found_response)

    def test_delete_type(self):
        """
            Unit test on delete_type route to deactivate a type
        """
        id = 2
        request = self.factory.delete(f"/type/delete/{id}")
        response = delete_type(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.type_deleted_response)

    def test_delete_not_found_type(self):
        """
            Unit test on delete_type route with the wrong id
        """
        id = 666
        request = self.factory.delete(f"/type/delete/{id}")
        response = delete_type(request, id)

        self.assertJSONEqual(response.content, self.type_not_found_response)

    def test_get_deactivated_types(self):
        """
            Unit test on get_types route with filter set to False
        """
        Type.objects.update(id=2, label="UnitTestType", is_activate=False)
        request = self.factory.get("/type/?isActivate=False")
        response = get_types(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.deactivated_types_response)

    def test_add_type(self):
        """
            Unit test on add_type route
        """
        request = self.factory.post("/type/add", data=self.type_add_payload, content_type='application/json')
        response = add_type(request)

        self.assertJSONEqual(response.content, self.type_add_response)

    def test_add_type_with_bad_payload(self):
        """
            Unit test on add_type route with bad payload
        """
        request = self.factory.post("/type/add", data=self.type_add_bad_payload, content_type='application/json')
        response = add_type(request)

        self.assertJSONEqual(response.content, self.type_add_bad_payload_response)

    def test_update_type(self):
        """
            Unit test on update_type route
        """
        request = self.factory.patch("/type/update", data=self.type_update_payload, content_type='application/json')
        response = update_type(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.type_update_response)

    def test_update_type_bad_payload(self):
        """
            Unit test on update_type route with bad payload
        """
        request = self.factory.patch("/type/update", data=self.type_update_bad_payload, content_type='application/json')
        response = update_type(request)

        self.assertJSONEqual(response.content, self.type_add_bad_payload_response)

    def test_update_type_on_type_not_found(self):
        """
            Unit test on update_type route with bad id in payload
        """
        request = self.factory.patch("/type/update", self.type_update_not_found_payload, content_type='application/json')
        response = update_type(request)

        self.assertJSONEqual(response.content, self.type_not_found_response)

    def test_get_types_with_bad_method(self):
        """
            Unit test on get_types route with bad request method
        """
        request = self.factory.post("/type/")
        response = get_types(request)

        self.assertJSONEqual(response.content, self.type_bad_method_on_get_response)

    def test_get_type_with_bad_method(self):
        """
            Unit test on get_type route with bad request method
        """
        id = 2
        request = self.factory.post(f"/type/details/{id}")
        response = get_type(request, id)

        self.assertJSONEqual(response.content, self.type_bad_method_on_get_response)

    def test_add_type_with_bad_method(self):
        """
            Unit test on add_type route with bad request method
        """
        request = self.factory.patch("/type/add", self.type_add_payload, content_type='application/json')
        response = add_type(request)

        self.assertJSONEqual(response.content, self.type_bad_method_on_post_response)

    def test_update_type_with_bad_method(self):
        """
            Unit test on update_type route with bad request method
        """
        request = self.factory.post("/type/update", self.type_update_payload, content_type='application/json')
        response = update_type(request)

        self.assertJSONEqual(response.content, self.type_bad_method_on_patch_response)

    def test_delete_type_with_bad_method(self):
        """
            Unit test on delete_type route with bad request method
        """
        id = 2
        request = self.factory.get(f"/type/delete/{id}")
        response = delete_type(request, id)

        self.assertJSONEqual(response.content, self.type_bad_method_on_delete_response)