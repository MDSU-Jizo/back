"""module to prevent pylint to return too-few-public-methods / R0903 error """
import dataclasses
import secrets

from django.db import models
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from contract.constants import Constants

backend = default_backend()
_ITERATIONS = 999999


class UserManager(BaseUserManager):
    """
        UserManager class
    """
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff set to True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser set to True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Class representing the User entity"""
    firstname = models.CharField(max_length=255, null=False)
    lastname = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.IntegerField(choices=Constants.GENDER_CHOICES, default=None, null=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    language = models.ForeignKey('language.Language', on_delete=models.CASCADE, default=1)
    role = models.ForeignKey(
        'role.Role',
        on_delete=models.CASCADE,
        default=Constants.Roles.ROLE_USER.value
    )
    time_before_creating = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: UserManager = UserManager()

    @dataclasses.dataclass
    class Meta:
        """Define the name of the table"""
        db_table = 'account'

    def __str__(self):
        return f'id: {self.pk}, Firstname: {self.firstname}, Lastname: {self.lastname}, Email: {self.email}'


def _derive_key(password: bytes, salt: bytes, iterations: int = _ITERATIONS) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))


def data_encrypt(message: bytes, password: str, iterations: int = _ITERATIONS) -> bytes:
    """Encrypt user's datas"""
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


# def data_decrypt(token: bytes, password: str) -> bytes:
#     decoded = b64d(token)
#     salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
#     iterations = int.from_bytes(iter, 'big')
#     key = _derive_key(password.encode(), salt, iterations)
#     return Fernet(key).decrypt(token)


def encrypt_profile(user):
    # key = base64.b64encode(bytes(user.email + user.email, 'utf-8'))
    key = str(user.email)
    user.firstname = data_encrypt(str(user.firstname).encode(), key)
    user.lastname = data_encrypt(str(user.lastname).encode(), key)
    user.email = data_encrypt(str(user.email).encode(), key)

    user.is_active = False
    user.save()


def get_list_of_users(is_active):
    return User.objects.raw(
        f"""
            SELECT
                a.id,
                a.firstname,
                a.lastname,
                a.email,
                a.birthdate,
                a.gender,
                a.country,
                a.date_joined,
                a.updated_at,
                a.language_id,
                l.label AS language_label,
                a.role_id,
                r.label AS role_label,
                a.is_active,
                a.date_joined,
                a.updated_at,
                a.last_login
            FROM account AS a
            LEFT JOIN language AS l ON l.id = a.language_id
            LEFT JOIN role AS r ON r.id = a.role_id
            WHERE a.is_active IS {is_active}
            ORDER BY a.id
        """
    )


def get_user_details(user_id):
    return User.objects.raw(
        f"""
            SELECT
                a.id,
                a.firstname,
                a.lastname,
                a.email,
                a.birthdate,
                a.gender,
                a.country,
                a.date_joined,
                a.updated_at,
                a.language_id,
                l.label AS language_label,
                a.role_id,
                r.label AS role_label,
                a.is_active,
                a.date_joined,
                a.updated_at,
                a.last_login
            FROM account AS a
            LEFT JOIN language AS l ON l.id = a.language_id
            LEFT JOIN role AS r ON r.id = a.role_id
            WHERE a.id = {user_id}
        """
    )