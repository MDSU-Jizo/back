"""
    Type Unit Tests
"""
from django.test import TestCase, RequestFactory
from .models import Role
from .views import get_roles, get_role, add_role, update_role, delete_role


class RoleTestCase(TestCase):
    """
        Test cases for Role API
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.role = Role.objects.create(id=2, label="UnitTestRole")
        self.activated_roles_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestRole",
                    "isActivate": True
                }
            ]
        }
        self.empty_role_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": []
        }
        self.deactivated_roles_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestRole",
                    "isActivate": False
                }
            ]
        }
        self.role_details_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": {
                "id": 2,
                "label": "UnitTestRole"
            }
        }
        self.role_not_found_response = {
            "code": 404,
            "result": "error",
            "message": "Role not found.",
            "data": []
        }
        self.role_deleted_response = {
            "code": 200,
            "result": "success",
            "message": "Role deleted successfully.",
            "data": []
        }
        self.role_add_payload = {
            "label": "UnitTestAddRole"
        }
        self.role_add_response = {
            "code": 201,
            "result": "success",
            "message": "Role created successfully.",
            "data": []
        }
        self.role_add_bad_payload = {
            "title": "UnitTestAddRole"
        }
        self.role_add_bad_payload_response = {
            "code": 500,
            "result": "error",
            "message": "Invalid form.",
            "data": {
                "label": [
                    "This field is required."
                ]
            }
        }
        self.role_update_payload = {
            "id": 2,
            "label": "UnitTestUpdateRole"
        }
        self.role_update_response = {
            "code": 200,
            "result": "success",
            "message": "Role updated successfully.",
            "data": []
        }
        self.role_update_bad_payload = {
            "id": 2,
            "title": "UnitTestUpdateRole"
        }
        self.role_update_not_found = {
            "id": 666,
            "label": "UnitTestUpdateRole"
        }
        self.role_bad_method_on_get_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a GET method.",
            "data": []
        }
        self.role_bad_method_on_post_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a POST method.",
            "data": []
        }
        self.role_bad_method_on_patch_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a PATCH method.",
            "data": []
        }
        self.role_bad_method_on_delete_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a DELETE method.",
            "data": []
        }

    def test_get_activated_roles(self):
        """
            Unit test on get_roles route without filter
        """
        request = self.factory.get("/role/")
        response = get_roles(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.activated_roles_response)

    def test_get_empty_roles(self):
        """
            Unit test on get_roles route with filter set to False while the database has no entity set to False
        """
        request = self.factory.get("/role/?isActivate=False")
        response = get_roles(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.empty_role_response)

    def test_get_role(self):
        """
            Unit test on get_role route
        """
        id = 2
        request = self.factory.get(f"/role/details/{id}")
        response = get_role(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.role_details_response)

    def test_get_role_not_found(self):
        """
            Unit test on get_role route with the wrong role id
        """
        id = 666
        request = self.factory.get(f"/role/{id}")
        response = get_role(request, id)

        self.assertJSONEqual(response.content, self.role_not_found_response)

    def test_delete_role(self):
        """
            Unit test on delete_role route to deactivate a role
        """
        id = 2
        request = self.factory.delete(f"/role/delete/{id}")
        response = delete_role(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.role_deleted_response)

    def test_delete_not_found_role(self):
        """
            Unit test on delete_role route with the wrong id
        """
        id = 666
        request = self.factory.delete(f"/role/delete/{id}")
        response = delete_role(request, id)

        self.assertJSONEqual(response.content, self.role_not_found_response)

    def test_get_deactivated_roles(self):
        """
            Unit test on get_roles route with filter set to False
        """
        Role.objects.update(id=2, label="UnitTestRole", is_activate=False)
        request = self.factory.get("/role/?isActivate=False")
        response = get_roles(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.deactivated_roles_response)

    def test_add_role(self):
        """
            Unit test on add_role route
        """
        request = self.factory.post("/role/add", data=self.role_add_payload, content_type='application/json')
        response = add_role(request)

        self.assertJSONEqual(response.content, self.role_add_response)

    def test_add_role_with_bad_payload(self):
        """
            Unit test on add_role route with bad payload
        """
        request = self.factory.post("/role/add", data=self.role_add_bad_payload, content_type='application/json')
        response = add_role(request)

        self.assertJSONEqual(response.content, self.role_add_bad_payload_response)

    def test_update_role(self):
        """
            Unit test on update_role route
        """
        request = self.factory.patch("/role/update", data=self.role_update_payload, content_type='application/json')
        response = update_role(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.role_update_response)

    def test_update_role_bad_payload(self):
        """
            Unit test on update_role route with bad payload
        """
        request = self.factory.patch("/role/update", data=self.role_update_bad_payload, content_type='application/json')
        response = update_role(request)

        self.assertJSONEqual(response.content, self.role_add_bad_payload_response)

    def test_update_role_on_role_not_found(self):
        """
            Unit test on update_role route with bad id in payload
        """
        request = self.factory.patch("/role/update", self.role_update_not_found, content_type='application/json')
        response = update_role(request)

        self.assertJSONEqual(response.content, self.role_not_found_response)

    def test_get_roles_with_bad_method(self):
        """
            Unit test on get_roles route with bad request method
        """
        request = self.factory.post("/role/")
        response = get_roles(request)

        self.assertJSONEqual(response.content, self.role_bad_method_on_get_response)

    def test_get_role_with_bad_method(self):
        """
            Unit test on get_role route with bad request method
        """
        id = 2
        request = self.factory.post(f"/role/details/{id}")
        response = get_role(request, id)

        self.assertJSONEqual(response.content, self.role_bad_method_on_get_response)

    def test_add_role_with_bad_method(self):
        """
            Unit test on add_role route with bad request method
        """
        request = self.factory.patch("/role/add", self.role_add_payload, content_type='application/json')
        response = add_role(request)

        self.assertJSONEqual(response.content, self.role_bad_method_on_post_response)

    def test_update_role_with_bad_method(self):
        """
            Unit test on update_role route with bad request method
        """
        request = self.factory.post("/role/update", self.role_update_payload, content_type='application/json')
        response = update_role(request)

        self.assertJSONEqual(response.content, self.role_bad_method_on_patch_response)

    def test_delete_role_with_bad_method(self):
        """
            Unit test on delete_role route with bad request method
        """
        id = 2
        request = self.factory.get(f"/role/delete/{id}")
        response = delete_role(request, id)

        self.assertJSONEqual(response.content, self.role_bad_method_on_delete_response)