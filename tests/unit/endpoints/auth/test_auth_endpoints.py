from datetime import datetime

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from meetups_backend.models import DbUserModel
from tests.utils.test_records_pks import TEST_USER_PASSWORD, TEST_USER_PK
from tests.utils.test_constants import DEFAULT_CONTENT_TYPE


class TestAuthEndpoints(TestCase):
    """
    This class contains tests that check "/auth" endpoints.
    """

    fixtures = ['test_user.json', ]

    def setUp(self):
        self.request_path: str = '/auth'
        self.user: DbUserModel = DbUserModel.objects.get(pk=TEST_USER_PK)

    def test_login(self):
        """
        Test the happy scenario of logging user in.
        """
        # send request to login endpoint
        request_data: dict = {'email': self.user.email, 'password': TEST_USER_PASSWORD}
        response: Response = self.client.post(
            path=f'{self.request_path}/login/',
            data=request_data,
            content_type=DEFAULT_CONTENT_TYPE
        )

        # check response format
        assert response.status_code == HTTP_200_OK
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'Login is successful.'
        assert isinstance(response.data['auth_token'], str)

        # check that user last login has been updated
        updated_user: DbUserModel = DbUserModel.objects.get(id=self.user.id)
        assert updated_user.last_login.date() == datetime.now().date()

    def test_login_not_found(self):
        """
        Test the case when user that is trying to login is not found.
        """
        request_data: dict = {'email': 'not_found@mail.com', 'password': 'not_found_password'}
        response: Response = self.client.post(
            path=f'{self.request_path}/login/',
            data=request_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data == {
            'status': 'error',
            'message': 'User with given credentials is not found.'
        }

    def test_login_invalid_email(self):
        """
        Test the case when given email is invalid.
        """
        request_data: dict = {'email': 'invalid', 'password': 'password'}
        response: Response = self.client.post(
            path=f'{self.request_path}/login/',
            data=request_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            'status': 'error',
            'message': 'Request body is invalid.',
            'invalid_keys': ['email'],
        }

    def test_login_too_short_password(self):
        """
        Test the case when given password is too short.
        """
        request_data: dict = {'email': self.user.email, 'password': 'short'}
        response: Response = self.client.post(
            path=f'{self.request_path}/login/',
            data=request_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            'status': 'error',
            'message': 'Request body is invalid.',
            'invalid_keys': ['password'],
        }
