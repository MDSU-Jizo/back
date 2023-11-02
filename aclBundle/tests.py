"""
    Type Unit Tests
"""
from django.test import TestCase, RequestFactory
from .models import AclBundle
from aclRoute.models import AclRoute
from aclBundle_aclRoute.models import AclBundleAclRoute
from .views import get_acl_bundles, get_acl_bundle, add_acl_bundle, update_acl_bundle, delete_acl_bundle


class AclBundleTestCase(TestCase):
    """
        Test cases for AclBundle API
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.acl_bundle = AclBundle.objects.create(id=2, label="UnitTestAclBundle")
        self.acl_route = AclRoute.objects.create(id=1, label="UnitTestAclRoute")
        self.bundle_route = AclBundleAclRoute.objects.create(id=1, acl_bundle_id=2, acl_route_id=1)
        self.activated_acl_bundles_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestAclBundle",
                    "routes": [
                        "UnitTestAclRoute"
                    ],
                    "isActivate": True
                }
            ]
        }
        self.empty_acl_bundle_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": []
        }
        self.deactivated_acl_bundles_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestAclBundle",
                    "routes": [
                        "UnitTestAclRoute"
                    ],
                    "isActivate": False
                }
            ]
        }
        self.acl_bundle_details_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": {
                "id": 2,
                "label": "UnitTestAclBundle",
                "routes": [
                    "UnitTestAclRoute"
                ],
                "isActivate": True
            }
        }
        self.acl_bundle_not_found_response = {
            "code": 404,
            "result": "error",
            "message": "AclBundle not found.",
            "data": []
        }
        self.acl_bundle_deleted_response = {
            "code": 200,
            "result": "success",
            "message": "AclBundle deleted successfully.",
            "data": []
        }
        self.acl_bundle_add_payload = {
            "label": "UnitTestAddAclBundle"
        }
        self.acl_bundle_add_response = {
            "code": 201,
            "result": "success",
            "message": "AclBundle created successfully.",
            "data": []
        }
        self.acl_bundle_add_bad_payload = {
            "title": "UnitTestAddAclBundle"
        }
        self.acl_bundle_add_bad_payload_response = {
            "code": 500,
            "result": "error",
            "message": "Invalid form.",
            "data": {
                "label": [
                    "This field is required."
                ]
            }
        }
        self.acl_bundle_update_payload = {
            "id": 2,
            "label": "UnitTestUpdateAclBundle"
        }
        self.acl_bundle_update_response = {
            "code": 200,
            "result": "success",
            "message": "AclBundle updated successfully.",
            "data": []
        }
        self.acl_bundle_update_bad_payload = {
            "id": 2,
            "title": "UnitTestUpdateAclBundle"
        }
        self.acl_bundle_update_not_found = {
            "id": 666,
            "label": "UnitTestUpdateAclBundle"
        }
        self.acl_bundle_bad_method_on_get_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a GET method.",
            "data": []
        }
        self.acl_bundle_bad_method_on_post_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a POST method.",
            "data": []
        }
        self.acl_bundle_bad_method_on_patch_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a PATCH method.",
            "data": []
        }
        self.acl_bundle_bad_method_on_delete_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a DELETE method.",
            "data": []
        }

    def test_get_activated_acl_bundles(self):
        """
            Unit test on get_acl_bundles route without filter
        """
        request = self.factory.get("/acl-bundle/")
        response = get_acl_bundles(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.activated_acl_bundles_response)

    def test_get_empty_acl_bundles(self):
        """
            Unit test on get_acl_bundles route with filter set to False while the database has no entity set to False
        """
        request = self.factory.get("/acl-bundle/?isActivate=False")
        response = get_acl_bundles(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.empty_acl_bundle_response)

    def test_get_acl_bundle(self):
        """
            Unit test on get_acl_bundle route
        """
        id = 2
        request = self.factory.get(f"/acl-bundle/details/{id}")
        response = get_acl_bundle(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.acl_bundle_details_response)

    def test_get_acl_bundle_not_found(self):
        """
            Unit test on get_acl_bundle route with the wrong acl_bundle id
        """
        id = 666
        request = self.factory.get(f"/acl-bundle/{id}")
        response = get_acl_bundle(request, id)

        self.assertJSONEqual(response.content, self.acl_bundle_not_found_response)

    def test_delete_acl_bundle(self):
        """
            Unit test on delete_acl_bundle route to deactivate a acl_bundle
        """
        id = 2
        request = self.factory.delete(f"/acl-bundle/delete/{id}")
        response = delete_acl_bundle(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.acl_bundle_deleted_response)

    def test_delete_not_found_acl_bundle(self):
        """
            Unit test on delete_acl_bundle route with the wrong id
        """
        id = 666
        request = self.factory.delete(f"/acl-bundle/delete/{id}")
        response = delete_acl_bundle(request, id)

        self.assertJSONEqual(response.content, self.acl_bundle_not_found_response)

    def test_get_deactivated_acl_bundles(self):
        """
            Unit test on get_acl_bundles route with filter set to False
        """
        AclBundle.objects.update(id=2, label="UnitTestAclBundle", is_activate=False)
        request = self.factory.get("/acl-bundle/?isActivate=False")
        response = get_acl_bundles(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.deactivated_acl_bundles_response)

    def test_add_acl_bundle(self):
        """
            Unit test on add_acl_bundle route
        """
        request = self.factory.post("/acl-bundle/add", data=self.acl_bundle_add_payload, content_type='application/json')
        response = add_acl_bundle(request)

        self.assertJSONEqual(response.content, self.acl_bundle_add_response)

    def test_add_acl_bundle_with_bad_payload(self):
        """
            Unit test on add_acl_bundle route with bad payload
        """
        request = self.factory.post("/acl-bundle/add", data=self.acl_bundle_add_bad_payload, content_type='application/json')
        response = add_acl_bundle(request)

        self.assertJSONEqual(response.content, self.acl_bundle_add_bad_payload_response)

    def test_update_acl_bundle(self):
        """
            Unit test on update_acl_bundle route
        """
        request = self.factory.patch("/acl-bundle/update", data=self.acl_bundle_update_payload, content_type='application/json')
        response = update_acl_bundle(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.acl_bundle_update_response)

    def test_update_acl_bundle_bad_payload(self):
        """
            Unit test on update_acl_bundle route with bad payload
        """
        request = self.factory.patch("/acl-bundle/update", data=self.acl_bundle_update_bad_payload, content_type='application/json')
        response = update_acl_bundle(request)

        self.assertJSONEqual(response.content, self.acl_bundle_add_bad_payload_response)

    def test_update_acl_bundle_on_acl_bundle_not_found(self):
        """
            Unit test on update_acl_bundle route with bad id in payload
        """
        request = self.factory.patch("/acl-bundle/update", self.acl_bundle_update_not_found, content_type='application/json')
        response = update_acl_bundle(request)

        self.assertJSONEqual(response.content, self.acl_bundle_not_found_response)

    def test_get_acl_bundles_with_bad_method(self):
        """
            Unit test on get_acl_bundles route with bad request method
        """
        request = self.factory.post("/acl-bundle/")
        response = get_acl_bundles(request)

        self.assertJSONEqual(response.content, self.acl_bundle_bad_method_on_get_response)

    def test_get_acl_bundle_with_bad_method(self):
        """
            Unit test on get_acl_bundle route with bad request method
        """
        id = 2
        request = self.factory.post(f"/acl-bundle/details/{id}")
        response = get_acl_bundle(request, id)

        self.assertJSONEqual(response.content, self.acl_bundle_bad_method_on_get_response)

    def test_add_acl_bundle_with_bad_method(self):
        """
            Unit test on add_acl_bundle route with bad request method
        """
        request = self.factory.patch("/acl-bundle/add", self.acl_bundle_add_payload, content_type='application/json')
        response = add_acl_bundle(request)

        self.assertJSONEqual(response.content, self.acl_bundle_bad_method_on_post_response)

    def test_update_acl_bundle_with_bad_method(self):
        """
            Unit test on update_acl_bundle route with bad request method
        """
        request = self.factory.post("/acl-bundle/update", self.acl_bundle_update_payload, content_type='application/json')
        response = update_acl_bundle(request)

        self.assertJSONEqual(response.content, self.acl_bundle_bad_method_on_patch_response)

    def test_delete_acl_bundle_with_bad_method(self):
        """
            Unit test on delete_acl_bundle route with bad request method
        """
        id = 2
        request = self.factory.get(f"/acl-bundle/delete/{id}")
        response = delete_acl_bundle(request, id)

        self.assertJSONEqual(response.content, self.acl_bundle_bad_method_on_delete_response)