import uuid

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from meetups_backend.models import DbUserModel
from meetups_backend.tools.auth_system_class import AuthSystem
from tests.utils.test_records_pks import TEST_USER_PK, TEST_USER_EMAIL, TEST_USER_PASSWORD
from tests.utils.test_constants import DEFAULT_CONTENT_TYPE


class TestDeleteUserEndpoint(TestCase):
    """
    This class contains tests that check DELETE "/users/{user_id}" endpoint.
    """

    fixtures = ['test_user.json', ]

    def setUp(self) -> None:
        self.request_path: str = '/users/'

        self.user = DbUserModel.objects.get(pk=TEST_USER_PK)

        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.auth_token: str = f'Bearer {auth_obj.jwt_token()}'

    def test_delete_user(self):
        """
        The test checks happy way of deleting a user.
        """
        response: Response = self.client.delete(
            path=f'{self.request_path}{self.user.id}/',
            HTTP_AUTHORIZATION=self.auth_token,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'status': 'success',
            'message': f'User with id {self.user.id} has been deleted successfully.'
        }

    def test_delete_user_not_found(self):
        """
        The test checks the case when requested user is not found.
        """
        not_found_user_id: str = str(uuid.uuid4())
        response: Response = self.client.delete(
            path=f'{self.request_path}{not_found_user_id}/',
            HTTP_AUTHORIZATION=self.auth_token,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data == {
            'status': 'error',
            'message': f'Resource with id {not_found_user_id} is not found.'
        }
