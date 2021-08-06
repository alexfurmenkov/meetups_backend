import uuid

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from meetups_backend.models import DbUserModel
from meetups_backend.tools.auth_system_class import AuthSystem
from tests.utils.test_records_pks import TEST_USER_PK, TEST_USER_EMAIL, TEST_USER_PASSWORD
from tests.utils.test_constants import DEFAULT_CONTENT_TYPE


class TestUpdateUserEndpoint(TestCase):
    """
    This class contains tests that check PUT "/users/{user_id}" endpoint.
    """
    fixtures = ['test_user.json', ]

    def setUp(self) -> None:
        self.request_path: str = '/users/'

        self.user = DbUserModel.objects.get(pk=TEST_USER_PK)

        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.auth_token: str = f'Bearer {auth_obj.jwt_token()}'

    def test_update_user(self):
        """
        Tests the happy scenario of updating a user.
        """
        request_data: dict = {
            'bio': 'Updated Bio'
        }
        response: Response = self.client.put(
            path=f'{self.request_path}{self.user.id}/',
            data=request_data,
            HTTP_AUTHORIZATION=self.auth_token,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'status': 'success',
            'message': f'User with id {self.user.id} has been updated successfully.'
        }

        updated_user: DbUserModel = DbUserModel.objects.get(id=self.user.id)
        assert updated_user.bio == request_data['bio']

    def test_update_user_not_found(self):
        """
        Tests the case when requested user is not found.
        """
        user_id: str = str(uuid.uuid4())
        request_data: dict = {
            'bio': 'Updated Bio'
        }
        response: Response = self.client.put(
            path=f'{self.request_path}{user_id}/',
            data=request_data,
            HTTP_AUTHORIZATION=self.auth_token,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data == {
            'status': 'error',
            'message': f'Resource with id {user_id} is not found.'
        }

    def test_update_user_invalid_request(self):
        """
        Test the case when the request contains invalid body.
        """
        request_data: dict = {
            'bio': {'invalid_key': 'invalid_value'}
        }
        response: Response = self.client.put(
            path=f'{self.request_path}{self.user.id}/',
            data=request_data,
            HTTP_AUTHORIZATION=self.auth_token,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            'status': 'error',
            'message': 'Request body is invalid.',
            'invalid_keys': ['bio']
        }
