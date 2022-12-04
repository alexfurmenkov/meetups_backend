import uuid

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from meetups_backend.models import DbUserModel
from meetups_backend.serializers.model_serializers import DbUserModelSerializer
from meetups_backend.tools.auth_system_class import AuthSystem
from tests.utils.test_records_pks import TEST_USER_PK, TEST_USER_EMAIL, TEST_USER_PASSWORD


class TestGetUsersEndpoints(TestCase):
    """
    This class contains tests that check GET "/users"
    and GET "/users/{user_id}" endpoints.
    """

    fixtures = ['test_user.json', ]

    def setUp(self) -> None:
        self.request_path: str = '/users/'

        self.user = DbUserModel.objects.get(pk=TEST_USER_PK)

        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.auth_token: str = f'Bearer {auth_obj.jwt_token()}'

    def test_list_users(self):
        """
        Tests the happy scenario of listing users.
        """
        response: Response = self.client.get(self.request_path, HTTP_AUTHORIZATION=self.auth_token)
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'status': 'success',
            'message': 'Users have been listed successfully.',
            'users': [DbUserModelSerializer(self.user).data]
        }

    def test_get_user_by_id(self):
        """
        Tests the happy scenario of getting a user by id.
        """
        response: Response = self.client.get(f'{self.request_path}{self.user.id}/', HTTP_AUTHORIZATION=self.auth_token)
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'status': 'success',
            'message': 'User have been retrieved successfully.',
            'user': DbUserModelSerializer(self.user).data
        }

    def test_get_user_by_id_not_found(self):
        """
        Tests case when requested user is not found.
        Expected behavior is response with 404 status and error message.
        """
        not_found_user_id: str = str(uuid.uuid4())
        response: Response = self.client.get(
            f'{self.request_path}{not_found_user_id}/',
            HTTP_AUTHORIZATION=self.auth_token
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data == {
            'status': 'error',
            'message': f'Resource with id {not_found_user_id} is not found.'
        }
