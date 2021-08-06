import jwt
from django.test import TestCase

from meetups_backend.models import DbUserModel
from meetups_backend.tools.auth_system_class import AuthSystem

from tests.utils.test_records_pks import TEST_USER_PK, TEST_USER_PASSWORD, TEST_USER_EMAIL


class TestAuthSystemClass(TestCase):
    """
    This class contains unit tests for AuthSystem class.
    """

    fixtures = ['test_user.json', ]

    def setUp(self):
        self.user: DbUserModel = DbUserModel.objects.get(pk=TEST_USER_PK)

    def test_authenticate_user(self):
        """
        The test checks authentication of a user.
        """
        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        assert auth_obj is not None
        assert isinstance(auth_obj, AuthSystem)

    def test_authenticate_user_not_found(self):
        """
        The test checks the case when the user is not found.
        """
        assert AuthSystem.authenticate_user('not_found@mail.com', 'not_found_password') is None

    def test_create_jwt_token(self):
        """
        The test checks creation of JWT token for an authenticated user.
        """
        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        jwt_token: str = auth_obj.jwt_token()

        assert isinstance(jwt_token, str)

        decoded_jwt_token: dict = jwt.decode(jwt_token, verify=False)
        assert decoded_jwt_token['user_id'] == str(self.user.id)
        assert decoded_jwt_token['username'] == self.user.email
        assert decoded_jwt_token['email'] == self.user.email
