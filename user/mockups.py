class MockUps:
    register_payload = {
        "firstname": "Unit",
        "lastname": "Test",
        "email": "unit.test@gmail.com",
        "password": "unit_test_123"
    }

    register_response = {
        "code": 201,
        "result": "success",
        "message": "User created successfully.",
        "data": ""
    }

    bad_method_on_get_response = {
        "code": 400,
        "result": "error",
        "message": "Must be a GET method.",
        "data": []
    }

    bad_method_on_post_response = {
        "code": 400,
        "result": "error",
        "message": "Must be a POST method.",
        "data": []
    }

    bad_method_on_patch_response = {
        "code": 400,
        "result": "error",
        "message": "Must be a PATCH method.",
        "data": []
    }

    bad_method_on_delete_response = {
        "code": 400,
        "result": "error",
        "message": "Must be a DELETE method.",
        "data": []
    }

    empty_payload = {
        "code": 400,
        "result": "error",
        "message": "Require a payload.",
        "data": []
    }

    register_bad_payload = {
        "firstname": "Axel",
        "lastname": "Pion",
        "email": "pionaxeltest3@gmail.com"
    }

    register_bad_payload_response = {
        "code": 400,
        "result": "error",
        "message": "Password required.",
        "data": []
    }

    register_email_already_exists_payload = {
        "firstname": "Axel",
        "lastname": "Pion",
        "email": "test.case@gmail.com",
        "password": "test123"
    }

    register_email_already_exists_response = {
        "code": 405,
        "result": "error",
        "message": "This email address already exists.",
        "data": []
    }

    login_payload = {
        "email": "test.case@gmail.com",
        "password": "test123"
    }

    login_bad_credential_on_email = {
        "email": "case.test@gmail.com",
        "password": "test123"
    }

    login_bad_credential_on_password = {
        "email": "test.case@gmail.com",
        "password": "123test"
    }

    login_response = {
        "code": 200,
        "result": "success",
        "message": "Logged in successfully.",
        "data": ""
    }

    login_no_password = {
        "email": "test.case@gmail.com"
    }

    login_no_password_response = {
        "code": 400,
        "result": "error",
        "message": "Password required.",
        "data": []
    }

    login_no_email = {
        "password": "test123"
    }

    login_no_email_response = {
        "code": 400,
        "result": "error",
        "message": "Email required.",
        "data": []
    }

    login_bad_credentials_response = {
        "code": 404,
        "result": "error",
        "message": "Bad credentials.",
        "data": []
    }

    get_profile_response = {
        "code": 200,
        "result": "success",
        "message": "",
        "data": {
            "id": 2,
            "firstname": "Axel",
            "lastname": "Pion",
            "email": "test.case@gmail.com",
            "birthdate": "1992-10-18",
            "gender": 1,
            "country": "France",
            "language": "French"
        }
    }

    user_not_found = {
        "code": 404,
        "result": "error",
        "message": "User not found.",
        "data": []
    }

    get_users_response = {
        "code": 200,
        "result": "success",
        "message": "",
        "data": [
            {
                "id": 2,
                "firstname": "Axel",
                "lastname": "Pion",
                "email": "test.case@gmail.com",
                "birthdate": "1992-10-18",
                "gender": 1,
                "country": "France",
                "language": {
                    "id": 1,
                    "label": "French"
                },
                "role": {
                    "id": 1,
                    "label": "ROLE_USER"
                },
                "is_active": True,
            }
        ]
    }

    get_users_not_found = {
        "code": 200,
        "result": "success",
        "message": "",
        "data": []
    }

    get_user_response = {
        "code": 200,
        "result": "success",
        "message": "",
        "data": {
            "id": 2,
            "firstname": "Axel",
            "lastname": "Pion",
            "email": "test.case@gmail.com",
            "birthdate": "1992-10-18",
            "gender": 1,
            "country": "France",
            "language": {
                "id": 1,
                "label": "French"
            },
            "role": {
                "id": 1,
                "label": "ROLE_USER"
            },
            "is_active": True,
        }
    }

    update_profile_payload = {
        "lastname": "Pion",
        "email": "test.case@gmail.com",
        "birthdate": "1992-10-29",
        "gender": 1,
        "country": "France"
    }

    update_profile_response = {
        "code": 200,
        "result": "success",
        "message": "User updated successfully.",
        "data": ""
    }

    update_profile_bad_payload = {
        "lastname": "Pion",
        "birthdate": "1992-10-29",
        "gender": 1,
        "country": "France"
    }

    update_profile_bad_payload_response = {
        "code": 500,
        "result": "error",
        "message": "Invalid form.",
        "data": {
            "email": [
                "This field is required."
            ]
        }
    }

    update_someone_else_profile_response = {
        "code": 403,
        "result": "error",
        "message": "You don't have the right to modify this profile.",
        "data": []
    }

    update_password_payload = {
        "actualPassword": "test123",
        "newPassword": "case123",
        "confirmPassword": "case123"
    }

    update_password_response = {
        "code": 200,
        "result": "success",
        "message": "Password updated successfully.",
        "data": []
    }

    update_password_bad_payload = {
        "newPassword": "case123",
        "confirmPassword": "case123"
    }

    update_password_bad_payload_response = {
        "code": 400,
        "result": "error",
        "message": "Invalid form.",
        "data": "actualPassword is required."
    }

    update_password_bad_actual_password = {
        "actualPassword": "case123",
        "newPassword": "test123",
        "confirmPassword": "test123"
    }

    update_password_bad_actual_password_response = {
        "code": 400,
        "result": "error",
        "message": "Incorrect actual password.",
        "data": []
    }

    update_password_bad_passwords = {
        "actualPassword": "test123",
        "newPassword": "case123",
        "confirmPassword": "cases123"
    }

    update_password_bad_passwords_response = {
        "code": 400,
        "result": "error",
        "message": "Passwords don't match.",
        "data": []
    }

    delete_profile_response = {
        "code": 200,
        "result": "success",
        "message": "Profile deleted successfully.",
        "data": []
    }

    change_language_payload = {
        "language": 2
    }

    change_language_response = {
        "code": 200,
        "result": "success",
        "message": "Language updated successfully.",
        "data": ""
    }

    change_language_bad_payload = {
        "langage": 2
    }

    change_language_bad_payload_response = {
        "code": 500,
        "result": "error",
        "message": "Invalid form.",
        "data": {
            "language": [
                "This field is required."
            ]
        }
    }

    change_language_not_found = {
        "language": 999
    }

    change_language_not_found_response = {
        "code": 500,
        "result": "error",
        "message": "Invalid form.",
        "data": {
            "language": [
                "Select a valid choice. That choice is not one of the available choices."
            ]
        }
    }
