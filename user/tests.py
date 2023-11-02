"""
    Itinerary Unit Tests
"""
import json

from django.test import TestCase, RequestFactory

from .models import User
from .views import (
    encode_user_as_jwt,
    register,
    login,
    get_profile,
    get_users,
    get_user,
    update_profile,
    update_password,
    delete_profile,
    change_language
)
from language.models import Language
from role.models import Role
from .mockups import MockUps
from passlib.hash import pbkdf2_sha256


class UserTestCase(TestCase):
    """
        Test cases for User API
    """

    def setUp(self):
        self.maxDiff = None
        self.factory = RequestFactory()
        self.language_french = Language.objects.create(id=1, label="French")
        self.language_english = Language.objects.create(id=2, label="English")
        self.role = Role.objects.create(id=1, label="ROLE_USER")
        self.password = pbkdf2_sha256.encrypt("test123")
        self.email = "test.case@gmail.com"
        self.user = User.objects.create(
            id=2,
            firstname="Axel",
            lastname="Pion",
            email=self.email,
            password=self.password,
            birthdate="1992-10-18",
            gender=1,
            country="France",
            language=self.language_french,
            role=self.role
        )
        self.token = encode_user_as_jwt(self.user)

    def test_encode_user_as_jwt(self):
        response = encode_user_as_jwt(self.user)

        self.assertTrue(isinstance(response, str))

    def test_register(self):
        request = self.factory.post(
            path="/user/register",
            data=MockUps.register_payload,
            content_type='application/json'
        )
        response = register(request)
        content = json.loads(response.content)

        self.assertTrue(isinstance(content, dict))
        self.assertEqual(content['code'], MockUps.register_response['code'])
        self.assertEqual(content['result'], MockUps.register_response['result'])
        self.assertEqual(content['message'], MockUps.register_response['message'])
        self.assertTrue(isinstance(content['data'], str))

    def test_register_bad_method(self):
        request = self.factory.get("/user/register")
        response = register(request)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_post_response)

    def test_register_without_payload(self):
        request = self.factory.post(path="/user/register", content_type='application/json')
        response = register(request)

        self.assertJSONEqual(response.content, MockUps.empty_payload)

    def test_register_bad_payload(self):
        request = self.factory.post(
            path="/user/register",
            data=MockUps.register_bad_payload,
            content_type='application/json'
        )
        response = register(request)

        self.assertJSONEqual(response.content, MockUps.register_bad_payload_response)

    def test_register_email_already_exists(self):
        request = self.factory.post(
            path="/user/register",
            data=MockUps.register_email_already_exists_payload,
            content_type='application/json'
        )
        response = register(request)

        self.assertJSONEqual(response.content, MockUps.register_email_already_exists_response)

    def test_login(self):
        request = self.factory.post(
            path="/user/login",
            data=MockUps.login_payload,
            content_type='application/json'
        )
        response = login(request)
        content = json.loads(response.content)

        self.assertTrue(isinstance(content, dict))
        self.assertEqual(content['code'], MockUps.login_response['code'])
        self.assertEqual(content['result'], MockUps.login_response['result'])
        self.assertEqual(content['message'], MockUps.login_response['message'])
        self.assertTrue(isinstance(content['data'], str))

    def test_login_bad_method(self):
        request = self.factory.get(
            path="/user/login"
        )
        response = login(request)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_post_response)

    def test_login_without_payload(self):
        request = self.factory.post(
            path="/user/login",
            content_type='application/json'
        )
        response = login(request)

        self.assertJSONEqual(response.content, MockUps.empty_payload)

    def test_login_no_email(self):
        request = self.factory.post(
            path="/user/login",
            data=MockUps.login_no_email,
            content_type='application/json'
        )
        response = login(request)

        self.assertJSONEqual(response.content, MockUps.login_no_email_response)

    def test_login_no_password(self):
        request = self.factory.post(
            path="/user/login",
            data=MockUps.login_no_password,
            content_type='application/json'
        )
        response = login(request)

        self.assertJSONEqual(response.content, MockUps.login_no_password_response)

    def test_login_wrong_email(self):
        request = self.factory.post(
            path="/user/login",
            data=MockUps.login_bad_credential_on_email,
            content_type='application/json'
        )
        response = login(request)

        self.assertJSONEqual(response.content, MockUps.login_bad_credentials_response)

    def test_login_wrong_password(self):
        request = self.factory.post(
            path="/user/login",
            data=MockUps.login_bad_credential_on_password,
            content_type='application/json'
        )
        response = login(request)

        self.assertJSONEqual(response.content, MockUps.login_bad_credentials_response)

    def test_get_profile(self):
        request = self.factory.get(
            path='/user/profile',
        )
        request.email = self.email
        response = get_profile(request)

        self.assertJSONEqual(response.content, MockUps.get_profile_response)

    def test_get_profile_bad_method(self):
        request = self.factory.delete(
            path='/user/profile',
        )
        response = get_profile(request)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_get_response)

    def test_get_profile_not_found(self):
        request = self.factory.get(
            path='/user/profile',
        )
        request.email = "test_case@gmail.com"
        response = get_profile(request)

        self.assertJSONEqual(response.content, MockUps.user_not_found)

    def test_get_users(self):
        request = self.factory.get(
            path='/user/',
        )
        response = get_users(request)
        users = json.loads(response.content)

        for user in users['data']:
            del user['date_joined']
            del user['updated_at']
            del user['last_login']

        self.assertJSONEqual(json.dumps(users), MockUps.get_users_response)

    def test_get_users_bad_method(self):
        request = self.factory.delete(
            path='/user/',
        )

        response = get_users(request)
        self.assertJSONEqual(response.content, MockUps.bad_method_on_get_response)

    def test_get_user(self):
        id = 2
        request = self.factory.get(
            path=f'/user/details/{id}',
        )
        response = get_user(request, id)
        user = json.loads(response.content)

        del user['data']['date_joined']
        del user['data']['updated_at']
        del user['data']['last_login']

        self.assertJSONEqual(json.dumps(user), MockUps.get_user_response)

    def test_get_user_bad_method(self):
        id = 2
        request = self.factory.delete(
            path=f'/user/details/{id}',
        )
        response = get_user(request, id)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_get_response)

    def test_get_user_not_found(self):
        id = 999
        request = self.factory.get(
            path=f'/user/details/{id}',
        )
        response = get_user(request, id)

        self.assertJSONEqual(response.content, MockUps.user_not_found)

    def test_update_profile(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/{id}',
            data=MockUps.update_profile_payload,
            content_type='application/json',
        )

        request.user_id = id

        response = update_profile(request, id)
        content = json.loads(response.content)
        self.token = content['data']

        self.assertTrue(isinstance(content, dict))
        self.assertEqual(content['code'], MockUps.update_profile_response['code'])
        self.assertEqual(content['result'], MockUps.update_profile_response['result'])
        self.assertEqual(content['message'], MockUps.update_profile_response['message'])
        self.assertTrue(isinstance(content['data'], str))

    def test_update_profile_bad_method(self):
        id = 2
        request = self.factory.get(
            path=f'/user/update/{id}',
            data=MockUps.update_profile_payload,
            content_type='application/json',
        )
        response = update_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_patch_response)

    def test_update_profile_without_payload(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/{id}',
            content_type='application/json',
        )
        response = update_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.empty_payload)

    def test_update_profile_bad_payload(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/{id}',
            data=MockUps.update_profile_bad_payload,
            content_type='application/json',
        )
        request.user_id = id
        response = update_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.update_profile_bad_payload_response)

    def test_update_someone_else_profile(self):
        id = 2
        user_id = 5
        request = self.factory.patch(
            path=f'/user/update/{id}',
            data=MockUps.update_profile_payload,
            content_type='application/json',
        )
        request.user_id = user_id
        response = update_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.update_someone_else_profile_response)

    def test_update_profile_not_found(self):
        id = 999
        user_id = 2
        request = self.factory.patch(
            path=f'/user/update/{id}',
            data=MockUps.update_profile_payload,
            content_type='application/json',
        )
        request.user_id = user_id
        response = update_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.user_not_found)

    def test_update_password(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/password/{id}',
            data=MockUps.update_password_payload,
            content_type='application/json'
        )
        request.user_id = id
        response = update_password(request, id)

        self.assertJSONEqual(response.content, MockUps.update_password_response)

    def test_update_password_bad_method(self):
        id = 2
        request = self.factory.post(
            path=f'/user/update/password/{id}',
            data=MockUps.update_password_payload,
            content_type='application/json'
        )
        request.user_id = id
        response = update_password(request, id)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_patch_response)

    def test_update_password_without_payload(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/password/{id}',
            content_type='application/json'
        )
        request.user_id = id
        response = update_password(request, id)

        self.assertJSONEqual(response.content, MockUps.empty_payload)

    def test_update_password_bad_payload(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/password/{id}',
            data=MockUps.update_password_bad_payload,
            content_type='application/json'
        )
        request.user_id = id
        response = update_password(request, id)

        self.assertJSONEqual(response.content, MockUps.update_password_bad_payload_response)

    def test_update_password_not_found(self):
        id = 999
        user_id = 2
        request = self.factory.patch(
            path=f'/user/update/password/{id}',
            data=MockUps.update_password_payload,
            content_type='application/json'
        )
        request.user_id = user_id
        response = update_password(request, id)

        self.assertJSONEqual(response.content, MockUps.update_someone_else_profile_response)

    def test_update_password_bad_actual_password(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/password/{id}',
            data=MockUps.update_password_bad_actual_password,
            content_type='application/json'
        )
        request.user_id = id
        response = update_password(request, id)

        self.assertJSONEqual(response.content, MockUps.update_password_bad_actual_password_response)

    def test_update_password_new_passwords_do_not_match(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/password/{id}',
            data=MockUps.update_password_bad_passwords,
            content_type='application/json'
        )
        request.user_id = id
        response = update_password(request, id)

        self.assertJSONEqual(response.content, MockUps.update_password_bad_passwords_response)

    def test_delete_profile(self):
        id = 2
        request = self.factory.delete(
            path=f'/user/delete/{id}',
        )
        request.user_id = id
        response = delete_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.delete_profile_response)

    def test_get_users_not_found(self):
        id = 999
        request = self.factory.delete(
            path=f'/user/delete/{id}',
        )
        request.user_id = id
        response = delete_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.user_not_found)

    def test_get_deactivated_users(self):
        request = self.factory.get(
            path='/user/?isActivate=False',
        )
        response = get_users(request)

        self.assertJSONEqual(response.content, MockUps.get_users_not_found)

    def test_delete_profile_bad_method(self):
        id = 2
        request = self.factory.get(
            path=f'/user/delete/{id}',
        )
        request.user_id = id
        response = delete_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_delete_response)

    def test_delete_profile_not_found(self):
        id = 999
        request = self.factory.delete(
            path=f'/user/delete/{id}',
        )
        request.user_id = id
        response = delete_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.user_not_found)

    def test_delete_someone_else_profile(self):
        id = 2
        userId = 3
        request = self.factory.delete(
            path=f'/user/delete/{id}',
        )
        request.user_id = userId
        response = delete_profile(request, id)

        self.assertJSONEqual(response.content, MockUps.update_someone_else_profile_response)

    def test_change_language(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/language/{id}',
            data=MockUps.change_language_payload,
            content_type="application/json"
        )
        request.user_id = id
        response = change_language(request, id)
        content = json.loads(response.content)
        self.token = content['data']

        self.assertTrue(isinstance(content, dict))
        self.assertEqual(content['code'], MockUps.change_language_response['code'])
        self.assertEqual(content['result'], MockUps.change_language_response['result'])
        self.assertEqual(content['message'], MockUps.change_language_response['message'])
        self.assertTrue(isinstance(content['data'], str))

    def test_change_language_bad_methods(self):
        id = 2
        request = self.factory.get(
            path=f'/user/update/language/{id}',
            data=MockUps.change_language_payload,
            content_type="application/json"
        )
        request.user_id = id
        response = change_language(request, id)

        self.assertJSONEqual(response.content, MockUps.bad_method_on_patch_response)

    def test_change_language_without_payload(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/language/{id}',
            content_type="application/json"
        )
        request.user_id = id
        response = change_language(request, id)

        self.assertJSONEqual(response.content, MockUps.empty_payload)

    def test_change_language_bad_payload(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/language/{id}',
            data=MockUps.change_language_bad_payload,
            content_type="application/json"
        )
        request.user_id = id
        response = change_language(request, id)

        self.assertJSONEqual(response.content, MockUps.change_language_bad_payload_response)

    def test_change_language_user_not_found(self):
        id = 999
        request = self.factory.patch(
            path=f'/user/update/language/{id}',
            data=MockUps.change_language_bad_payload,
            content_type="application/json"
        )
        request.user_id = id
        response = change_language(request, id)

        self.assertJSONEqual(response.content, MockUps.user_not_found)

    def test_change_language_not_found(self):
        id = 2
        request = self.factory.patch(
            path=f'/user/update/language/{id}',
            data=MockUps.change_language_not_found,
            content_type="application/json"
        )
        request.user_id = id
        response = change_language(request, id)

        self.assertJSONEqual(response.content, MockUps.change_language_not_found_response)

    def test_change_someone_else_language(self):
        id = 2
        userId = 3
        request = self.factory.patch(
            path=f'/user/update/language/{id}',
            data=MockUps.change_language_bad_payload,
            content_type="application/json"
        )
        request.user_id = userId
        response = change_language(request, id)

        self.assertJSONEqual(response.content, MockUps.update_someone_else_profile_response)
