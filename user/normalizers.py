"""
    User normalizers
"""


def jwt_normalizer(user, expiration_date) -> dict:
    """
        Function to return JWT as formatted data

        Args:
            user
        Returns:
             data about user as dict
    """
    return {
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "language": {
            "id": user.language.id,
            "label": user.language.label,
        },
        "role": {
            "id": user.role.id,
            "label": user.role.label,
        },
        "expires_at": str(expiration_date)
    }


def profile_normalizer(user) -> dict:
    return {
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "birthdate": user.birthdate,
        "gender": user.gender,
        "country": user.country,
        "language": user.language.label
    }


def users_normalizer(users) -> list:
    result = []

    for user in users:
        item = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "birthdate": user.birthdate,
            "gender": user.gender,
            "country": user.country,
            "language": {
                "id": user.language.id,
                "label": user.language.label,
            },
            "role": {
                "id": user.role.id,
                "label": user.role.label,
            },
            "is_active": user.is_active,
            "date_joined": user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": user.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "last_login": user.last_login,
        }

        result.append(item)

    return result


def user_normalizer(user) -> dict:
    for data in user:
        return {
            "id": data.id,
            "firstname": data.firstname,
            "lastname": data.lastname,
            "email": data.email,
            "birthdate": data.birthdate,
            "gender": data.gender,
            "country": data.country,
            "language": {
                "id": data.language.id,
                "label": data.language.label,
            },
            "role": {
                "id": data.role.id,
                "label": data.role.label,
            },
            "is_active": data.is_active,
            "date_joined": data.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": data.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "last_login": data.last_login,
        }
