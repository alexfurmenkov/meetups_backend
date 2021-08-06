from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from meetups_backend.models import DbUserModel
from tests.utils.test_records_pks import TEST_USER_PK
from tests.utils.test_constants import DEFAULT_CONTENT_TYPE


class TestCreateUserEndpoint(TestCase):
    """
    This class contains tests that check POST "/users" endpoint.
    """

    fixtures = ['test_user.json', ]

    def setUp(self) -> None:
        self.request_path: str = '/users/'
        self.user = DbUserModel.objects.get(pk=TEST_USER_PK)

    def test_create_new_user(self):
        """
        Tests the happy scenario of creating a user.
        """
        request_data: dict = {
            'email': 'test@mail.com',
            'password': 'test_password',
            'bio': 'Test Personal Info'
        }
        response: Response = self.client.post(
            path=self.request_path,
            data=request_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_201_CREATED
        assert response.data['status'] == 'success'
        assert response.data['message'] == f'User with email {request_data["email"]} has been created successfully.'

        created_user: DbUserModel = DbUserModel.objects.get(id=response.data['id'])
        assert created_user.email == request_data['email']
        assert created_user.bio == request_data['bio']

    def test_create_new_user_existing_user(self):
        """
        Tests the case when the user exists. Expected behavior is
        a response with 400 HTTP status and error message.
        """
        request_data: dict = {
            'email': self.user.email,
            'password': self.user.password,
            'bio': self.user.bio
        }
        response: Response = self.client.post(
            path=self.request_path,
            data=request_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert response.data['message'] == f'User with email {request_data["email"]} already exists.'

    def test_create_new_user_no_mandatory_fields(self):
        """
        Tests the case when request body is missing password and bio.
        Expected behavior is a response with 400 HTTP status and error message.
        """
        new_user_data: dict = {
            'email': 'test@mail.com',
        }
        response: Response = self.client.post(
            path=self.request_path,
            data=new_user_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == 400
        assert response.data == {
            'status': 'error',
            'message': 'Request body is invalid.',
            'invalid_keys': ['password', 'bio']
        }

    def test_create_new_user_invalid_email(self):
        """
        Tests the case when request body contains invalid email.
        Expected behavior is a response with 400 HTTP status and error message.
        """
        new_user_data: dict = {
            'email': 'test',
            'password': 'test_password',
            'bio': 'Test Personal Info'
        }
        response: Response = self.client.post(
            path=self.request_path,
            data=new_user_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == 400
        assert response.data == {
            'status': 'error',
            'message': 'Request body is invalid.',
            'invalid_keys': ['email']
        }

    def test_create_new_user_too_short_password(self):
        """
        Tests the case when request body contains too short password (min length is 6 chars).
        Expected behavior is a response with 400 HTTP status and error message.
        """
        new_user_data: dict = {
            'email': 'test@mail.com',
            'password': 'short',
            'bio': 'Test Personal Info'
        }
        response: Response = self.client.post(
            path=self.request_path,
            data=new_user_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert response.status_code == 400
        assert response.data == {
            'status': 'error',
            'message': 'Request body is invalid.',
            'invalid_keys': ['password']
        }
