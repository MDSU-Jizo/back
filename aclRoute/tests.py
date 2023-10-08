"""
    Type Unit Tests
"""
from django.test import TestCase, RequestFactory
from .models import AclRoute
from .views import get_acl_routes, get_acl_route, add_acl_route, update_acl_route, delete_acl_route


class AclRouteTestCase(TestCase):
    """
        Test cases for AclRoute API
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.acl_route = AclRoute.objects.create(id=2, label="UnitTestAclRoute")
        self.activated_acl_routes_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestAclRoute",
                    "isActivate": True
                }
            ]
        }
        self.empty_acl_route_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": []
        }
        self.deactivated_acl_routes_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestAclRoute",
                    "isActivate": False
                }
            ]
        }
        self.acl_route_details_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": {
                "id": 2,
                "label": "UnitTestAclRoute"
            }
        }
        self.acl_route_not_found_response = {
            "code": 404,
            "result": "error",
            "message": "AclRoute not found.",
            "data": []
        }
        self.acl_route_deleted_response = {
            "code": 200,
            "result": "success",
            "message": "AclRoute deleted successfully.",
            "data": []
        }
        self.acl_route_add_payload = {
            "label": "UnitTestAddAclRoute"
        }
        self.acl_route_add_response = {
            "code": 201,
            "result": "success",
            "message": "AclRoute created successfully.",
            "data": []
        }
        self.acl_route_add_bad_payload = {
            "title": "UnitTestAddAclRoute"
        }
        self.acl_route_add_bad_payload_response = {
            "code": 500,
            "result": "error",
            "message": "Invalid form.",
            "data": {
                "label": [
                    "This field is required."
                ]
            }
        }
        self.acl_route_update_payload = {
            "id": 2,
            "label": "UnitTestUpdateAclRoute"
        }
        self.acl_route_update_response = {
            "code": 200,
            "result": "success",
            "message": "AclRoute updated successfully.",
            "data": []
        }
        self.acl_route_update_bad_payload = {
            "id": 2,
            "title": "UnitTestUpdateAclRoute"
        }
        self.acl_route_update_not_found = {
            "id": 666,
            "label": "UnitTestUpdateAclRoute"
        }
        self.acl_route_bad_method_on_get_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a GET method.",
            "data": []
        }
        self.acl_route_bad_method_on_post_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a POST method.",
            "data": []
        }
        self.acl_route_bad_method_on_patch_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a PATCH method.",
            "data": []
        }
        self.acl_route_bad_method_on_delete_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a DELETE method.",
            "data": []
        }

    def test_get_activated_acl_routes(self):
        """
            Unit test on get_acl_routes route without filter
        """
        request = self.factory.get("/acl-route/")
        response = get_acl_routes(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.activated_acl_routes_response)

    def test_get_empty_acl_routes(self):
        """
            Unit test on get_acl_routes route with filter set to False while the database has no entity set to False
        """
        request = self.factory.get("/acl-route/?isActivate=False")
        response = get_acl_routes(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.empty_acl_route_response)

    def test_get_acl_route(self):
        """
            Unit test on get_acl_route route
        """
        id = 2
        request = self.factory.get(f"/acl-route/details/{id}")
        response = get_acl_route(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.acl_route_details_response)

    def test_get_acl_route_not_found(self):
        """
            Unit test on get_acl_route route with the wrong acl_route id
        """
        id = 666
        request = self.factory.get(f"/acl-route/{id}")
        response = get_acl_route(request, id)

        self.assertJSONEqual(response.content, self.acl_route_not_found_response)

    def test_delete_acl_route(self):
        """
            Unit test on delete_acl_route route to deactivate a acl_route
        """
        id = 2
        request = self.factory.delete(f"/acl-route/delete/{id}")
        response = delete_acl_route(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.acl_route_deleted_response)

    def test_delete_not_found_acl_route(self):
        """
            Unit test on delete_acl_route route with the wrong id
        """
        id = 666
        request = self.factory.delete(f"/acl-route/delete/{id}")
        response = delete_acl_route(request, id)

        self.assertJSONEqual(response.content, self.acl_route_not_found_response)

    def test_get_deactivated_acl_routes(self):
        """
            Unit test on get_acl_routes route with filter set to False
        """
        AclRoute.objects.update(id=2, label="UnitTestAclRoute", is_activate=False)
        request = self.factory.get("/acl-route/?isActivate=False")
        response = get_acl_routes(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.deactivated_acl_routes_response)

    def test_add_acl_route(self):
        """
            Unit test on add_acl_route route
        """
        request = self.factory.post("/acl-route/add", data=self.acl_route_add_payload, content_type='application/json')
        response = add_acl_route(request)

        self.assertJSONEqual(response.content, self.acl_route_add_response)

    def test_add_acl_route_with_bad_payload(self):
        """
            Unit test on add_acl_route route with bad payload
        """
        request = self.factory.post("/acl-route/add", data=self.acl_route_add_bad_payload, content_type='application/json')
        response = add_acl_route(request)

        self.assertJSONEqual(response.content, self.acl_route_add_bad_payload_response)

    def test_update_acl_route(self):
        """
            Unit test on update_acl_route route
        """
        request = self.factory.patch("/acl-route/update", data=self.acl_route_update_payload, content_type='application/json')
        response = update_acl_route(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.acl_route_update_response)

    def test_update_acl_route_bad_payload(self):
        """
            Unit test on update_acl_route route with bad payload
        """
        request = self.factory.patch("/acl-route/update", data=self.acl_route_update_bad_payload, content_type='application/json')
        response = update_acl_route(request)

        self.assertJSONEqual(response.content, self.acl_route_add_bad_payload_response)

    def test_update_acl_route_on_acl_route_not_found(self):
        """
            Unit test on update_acl_route route with bad id in payload
        """
        request = self.factory.patch("/acl-route/update", self.acl_route_update_not_found, content_type='application/json')
        response = update_acl_route(request)

        self.assertJSONEqual(response.content, self.acl_route_not_found_response)

    def test_get_acl_routes_with_bad_method(self):
        """
            Unit test on get_acl_routes route with bad request method
        """
        request = self.factory.post("/acl-route/")
        response = get_acl_routes(request)

        self.assertJSONEqual(response.content, self.acl_route_bad_method_on_get_response)

    def test_get_acl_route_with_bad_method(self):
        """
            Unit test on get_acl_route route with bad request method
        """
        id = 2
        request = self.factory.post(f"/acl-route/details/{id}")
        response = get_acl_route(request, id)

        self.assertJSONEqual(response.content, self.acl_route_bad_method_on_get_response)

    def test_add_acl_route_with_bad_method(self):
        """
            Unit test on add_acl_route route with bad request method
        """
        request = self.factory.patch("/acl-route/add", self.acl_route_add_payload, content_type='application/json')
        response = add_acl_route(request)

        self.assertJSONEqual(response.content, self.acl_route_bad_method_on_post_response)

    def test_update_acl_route_with_bad_method(self):
        """
            Unit test on update_acl_route route with bad request method
        """
        request = self.factory.post("/acl-route/update", self.acl_route_update_payload, content_type='application/json')
        response = update_acl_route(request)

        self.assertJSONEqual(response.content, self.acl_route_bad_method_on_patch_response)

    def test_delete_acl_route_with_bad_method(self):
        """
            Unit test on delete_acl_route route with bad request method
        """
        id = 2
        request = self.factory.get(f"/acl-route/delete/{id}")
        response = delete_acl_route(request, id)

        self.assertJSONEqual(response.content, self.acl_route_bad_method_on_delete_response)