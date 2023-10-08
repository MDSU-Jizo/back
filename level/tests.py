"""
    Type Unit Tests
"""
from django.test import TestCase, RequestFactory
from .models import Level
from .views import get_levels, get_level, add_level, update_level, delete_level


class LevelTestCase(TestCase):
    """
        Test cases for Level API
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.level = Level.objects.create(id=2, label="UnitTestLevel")
        self.activated_levels_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestLevel",
                    "isActivate": True
                }
            ]
        }
        self.empty_level_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": []
        }
        self.deactivated_levels_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestLevel",
                    "isActivate": False
                }
            ]
        }
        self.level_details_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": {
                "id": 2,
                "label": "UnitTestLevel"
            }
        }
        self.level_not_found_response = {
            "code": 404,
            "result": "error",
            "message": "Level not found.",
            "data": []
        }
        self.level_deleted_response = {
            "code": 200,
            "result": "success",
            "message": "Level deleted successfully.",
            "data": []
        }
        self.level_add_payload = {
            "label": "UnitTestAddLevel"
        }
        self.level_add_response = {
            "code": 201,
            "result": "success",
            "message": "Level created successfully.",
            "data": []
        }
        self.level_add_bad_payload = {
            "title": "UnitTestAddLevel"
        }
        self.level_add_bad_payload_response = {
            "code": 500,
            "result": "error",
            "message": "Invalid form.",
            "data": {
                "label": [
                    "This field is required."
                ]
            }
        }
        self.level_update_payload = {
            "id": 2,
            "label": "UnitTestUpdateLevel"
        }
        self.level_update_response = {
            "code": 200,
            "result": "success",
            "message": "Level updated successfully.",
            "data": []
        }
        self.level_update_bad_payload = {
            "id": 2,
            "title": "UnitTestUpdateLevel"
        }
        self.level_update_not_found = {
            "id": 666,
            "label": "UnitTestUpdateLevel"
        }
        self.level_bad_method_on_get_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a GET method.",
            "data": []
        }
        self.level_bad_method_on_post_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a POST method.",
            "data": []
        }
        self.level_bad_method_on_patch_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a PATCH method.",
            "data": []
        }
        self.level_bad_method_on_delete_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a DELETE method.",
            "data": []
        }

    def test_get_activated_levels(self):
        """
            Unit test on get_levels route without filter
        """
        request = self.factory.get("/level/")
        response = get_levels(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.activated_levels_response)

    def test_get_empty_levels(self):
        """
            Unit test on get_levels route with filter set to False while the database has no entity set to False
        """
        request = self.factory.get("/level/?isActivate=False")
        response = get_levels(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.empty_level_response)

    def test_get_level(self):
        """
            Unit test on get_level route
        """
        id = 2
        request = self.factory.get(f"/level/details/{id}")
        response = get_level(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.level_details_response)

    def test_get_level_not_found(self):
        """
            Unit test on get_level route with the wrong level id
        """
        id = 666
        request = self.factory.get(f"/level/{id}")
        response = get_level(request, id)

        self.assertJSONEqual(response.content, self.level_not_found_response)

    def test_delete_level(self):
        """
            Unit test on delete_level route to deactivate a level
        """
        id = 2
        request = self.factory.delete(f"/level/delete/{id}")
        response = delete_level(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.level_deleted_response)

    def test_delete_not_found_level(self):
        """
            Unit test on delete_level route with the wrong id
        """
        id = 666
        request = self.factory.delete(f"/level/delete/{id}")
        response = delete_level(request, id)

        self.assertJSONEqual(response.content, self.level_not_found_response)

    def test_get_deactivated_levels(self):
        """
            Unit test on get_levels route with filter set to False
        """
        Level.objects.update(id=2, label="UnitTestLevel", is_activate=False)
        request = self.factory.get("/level/?isActivate=False")
        response = get_levels(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.deactivated_levels_response)

    def test_add_level(self):
        """
            Unit test on add_level route
        """
        request = self.factory.post("/level/add", data=self.level_add_payload, content_type='application/json')
        response = add_level(request)

        self.assertJSONEqual(response.content, self.level_add_response)

    def test_add_level_with_bad_payload(self):
        """
            Unit test on add_level route with bad payload
        """
        request = self.factory.post("/level/add", data=self.level_add_bad_payload, content_type='application/json')
        response = add_level(request)

        self.assertJSONEqual(response.content, self.level_add_bad_payload_response)

    def test_update_level(self):
        """
            Unit test on update_level route
        """
        request = self.factory.patch("/level/update", data=self.level_update_payload, content_type='application/json')
        response = update_level(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.level_update_response)

    def test_update_level_bad_payload(self):
        """
            Unit test on update_level route with bad payload
        """
        request = self.factory.patch("/level/update", data=self.level_update_bad_payload, content_type='application/json')
        response = update_level(request)

        self.assertJSONEqual(response.content, self.level_add_bad_payload_response)

    def test_update_level_on_level_not_found(self):
        """
            Unit test on update_level route with bad id in payload
        """
        request = self.factory.patch("/level/update", self.level_update_not_found, content_type='application/json')
        response = update_level(request)

        self.assertJSONEqual(response.content, self.level_not_found_response)

    def test_get_levels_with_bad_method(self):
        """
            Unit test on get_levels route with bad request method
        """
        request = self.factory.post("/level/")
        response = get_levels(request)

        self.assertJSONEqual(response.content, self.level_bad_method_on_get_response)

    def test_get_level_with_bad_method(self):
        """
            Unit test on get_level route with bad request method
        """
        id = 2
        request = self.factory.post(f"/level/details/{id}")
        response = get_level(request, id)

        self.assertJSONEqual(response.content, self.level_bad_method_on_get_response)

    def test_add_level_with_bad_method(self):
        """
            Unit test on add_level route with bad request method
        """
        request = self.factory.patch("/level/add", self.level_add_payload, content_type='application/json')
        response = add_level(request)

        self.assertJSONEqual(response.content, self.level_bad_method_on_post_response)

    def test_update_level_with_bad_method(self):
        """
            Unit test on update_level route with bad request method
        """
        request = self.factory.post("/level/update", self.level_update_payload, content_type='application/json')
        response = update_level(request)

        self.assertJSONEqual(response.content, self.level_bad_method_on_patch_response)

    def test_delete_level_with_bad_method(self):
        """
            Unit test on delete_level route with bad request method
        """
        id = 2
        request = self.factory.get(f"/level/delete/{id}")
        response = delete_level(request, id)

        self.assertJSONEqual(response.content, self.level_bad_method_on_delete_response)