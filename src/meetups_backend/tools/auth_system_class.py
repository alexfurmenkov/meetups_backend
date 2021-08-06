from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings

from meetups_backend.models import DbUserModel


class AuthSystem:
    """
    This class performs operations related to authentication.
    Authenticates users, generates JWT tokens.

    Example:
    auth_obj: AuthSystem = AuthSystem.authenticate_user(email, password)
    auth_obj.jwt_token()
    """

    def __init__(self, user: DbUserModel):
        self._user = user

    @classmethod
    def authenticate_user(cls, email: str, password: str):
        """
        Authenticates a user and returns AuthSystem instance.
        """
        user: DbUserModel = authenticate(username=email, password=password)
        if not user:
            return None
        return cls(user)

    def jwt_token(self) -> str:
        """
        Generates a JWT token.
        """
        payload = api_settings.JWT_PAYLOAD_HANDLER(self._user)
        jwt_token: str = api_settings.JWT_ENCODE_HANDLER(payload)
        return jwt_token

    def update_last_login_date(self):
        """
        Updates last login field in user record.
        """
        update_last_login(None, self._user)
