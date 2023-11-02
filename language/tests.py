"""
    Language Unit Tests
"""
from django.test import TestCase, RequestFactory
from .models import Language
from .views import get_languages, get_language, add_language, update_language, delete_language


class LanguageTestCase(TestCase):
    """
        Test cases for Language API
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.language = Language.objects.create(id=2, label="UnitTestLanguage")
        self.activated_languages_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestLanguage",
                    "isActivate": True
                }
            ]
        }
        self.empty_language_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": []
        }
        self.deactivated_languages_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": [
                {
                    "id": 2,
                    "label": "UnitTestLanguage",
                    "isActivate": False
                }
            ]
        }
        self.language_details_response = {
            "code": 200,
            "result": "success",
            "message": "",
            "data": {
                "id": 2,
                "label": "UnitTestLanguage"
            }
        }
        self.language_not_found_response = {
            "code": 404,
            "result": "error",
            "message": "Language not found.",
            "data": []
        }
        self.language_deleted_response = {
            "code": 200,
            "result": "success",
            "message": "Language deleted successfully.",
            "data": []
        }
        self.language_add_payload = {
            "label": "UnitTestAddLanguage"
        }
        self.language_add_response = {
            "code": 201,
            "result": "success",
            "message": "Language created successfully.",
            "data": []
        }
        self.language_add_bad_payload = {
            "title": "UnitTestAddLanguage"
        }
        self.language_add_bad_payload_response = {
            "code": 500,
            "result": "error",
            "message": "Invalid form.",
            "data": {
                "label": [
                    "This field is required."
                ]
            }
        }
        self.language_update_payload = {
            "id": 2,
            "label": "UnitTestUpdateLanguage"
        }
        self.language_update_response = {
            "code": 200,
            "result": "success",
            "message": "Language updated successfully.",
            "data": []
        }
        self.language_update_bad_payload = {
            "id": 2,
            "title": "UnitTestUpdateLanguage"
        }
        self.language_update_not_found = {
            "id": 666,
            "label": "UnitTestUpdateLanguage"
        }
        self.language_bad_method_on_get_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a GET method.",
            "data": []
        }
        self.language_bad_method_on_post_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a POST method.",
            "data": []
        }
        self.language_bad_method_on_patch_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a PATCH method.",
            "data": []
        }
        self.language_bad_method_on_delete_response = {
            "code": 400,
            "result": "error",
            "message": "Must be a DELETE method.",
            "data": []
        }

    def test_get_activated_languages(self):
        """
            Unit test on get_languages route without filter
        """
        request = self.factory.get("/language/")
        response = get_languages(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.activated_languages_response)

    def test_get_empty_languages(self):
        """
            Unit test on get_languages route with filter set to False while the database has no entity set to False
        """
        request = self.factory.get("/language/?isActivate=False")
        response = get_languages(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.empty_language_response)

    def test_get_language(self):
        """
            Unit test on get_language route
        """
        id = 2
        request = self.factory.get(f"/language/details/{id}")
        response = get_language(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.language_details_response)

    def test_get_language_not_found(self):
        """
            Unit test on get_language route with the wrong language id
        """
        id = 666
        request = self.factory.get(f"/language/{id}")
        response = get_language(request, id)

        self.assertJSONEqual(response.content, self.language_not_found_response)

    def test_delete_language(self):
        """
            Unit test on delete_language route to deactivate a language
        """
        id = 2
        request = self.factory.delete(f"/language/delete/{id}")
        response = delete_language(request, id)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.language_deleted_response)

    def test_delete_not_found_language(self):
        """
            Unit test on delete_language route with the wrong id
        """
        id = 666
        request = self.factory.delete(f"/language/delete/{id}")
        response = delete_language(request, id)

        self.assertJSONEqual(response.content, self.language_not_found_response)

    def test_get_deactivated_languages(self):
        """
            Unit test on get_languages route with filter set to False
        """
        Language.objects.update(id=2, label="UnitTestLanguage", is_activate=False)
        request = self.factory.get("/language/?isActivate=False")
        response = get_languages(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.deactivated_languages_response)

    def test_add_language(self):
        """
            Unit test on add_language route
        """
        request = self.factory.post("/language/add", data=self.language_add_payload, content_type='application/json')
        response = add_language(request)

        self.assertJSONEqual(response.content, self.language_add_response)

    def test_add_language_with_bad_payload(self):
        """
            Unit test on add_language route with bad payload
        """
        request = self.factory.post("/language/add", data=self.language_add_bad_payload, content_type='application/json')
        response = add_language(request)

        self.assertJSONEqual(response.content, self.language_add_bad_payload_response)

    def test_update_language(self):
        """
            Unit test on update_language route
        """
        request = self.factory.patch("/language/update", data=self.language_update_payload, content_type='application/json')
        response = update_language(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.language_update_response)

    def test_update_language_bad_payload(self):
        """
            Unit test on update_language route with bad payload
        """
        request = self.factory.patch("/language/update", data=self.language_update_bad_payload, content_type='application/json')
        response = update_language(request)

        self.assertJSONEqual(response.content, self.language_add_bad_payload_response)

    def test_update_language_on_language_not_found(self):
        """
            Unit test on update_language route with bad id in payload
        """
        request = self.factory.patch("/language/update", self.language_update_not_found, content_type='application/json')
        response = update_language(request)

        self.assertJSONEqual(response.content, self.language_not_found_response)

    def test_get_languages_with_bad_method(self):
        """
            Unit test on get_languages route with bad request method
        """
        request = self.factory.post("/language/")
        response = get_languages(request)

        self.assertJSONEqual(response.content, self.language_bad_method_on_get_response)

    def test_get_language_with_bad_method(self):
        """
            Unit test on get_language route with bad request method
        """
        id = 2
        request = self.factory.post(f"/language/details/{id}")
        response = get_language(request, id)

        self.assertJSONEqual(response.content, self.language_bad_method_on_get_response)

    def test_add_language_with_bad_method(self):
        """
            Unit test on add_language route with bad request method
        """
        request = self.factory.patch("/language/add", self.language_add_payload, content_type='application/json')
        response = add_language(request)

        self.assertJSONEqual(response.content, self.language_bad_method_on_post_response)

    def test_update_language_with_bad_method(self):
        """
            Unit test on update_language route with bad request method
        """
        request = self.factory.post("/language/update", self.language_update_payload, content_type='application/json')
        response = update_language(request)

        self.assertJSONEqual(response.content, self.language_bad_method_on_patch_response)

    def test_delete_language_with_bad_method(self):
        """
            Unit test on delete_language route with bad request method
        """
        id = 2
        request = self.factory.get(f"/language/delete/{id}")
        response = delete_language(request, id)

        self.assertJSONEqual(response.content, self.language_bad_method_on_delete_response)