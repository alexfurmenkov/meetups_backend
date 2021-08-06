from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from meetups_backend.models import DbPostModel, DbPostTypeModel
from meetups_backend.tools.auth_system_class import AuthSystem
from tests.utils.test_records_pks import TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_POST_TYPE_PK
from tests.utils.test_constants import DEFAULT_CONTENT_TYPE


class TestCreateNewPost(TestCase):
    """
    This class contains tests that check POST "/posts" endpoint.
    """

    fixtures = ['test_user.json', 'test_post_type.json', ]

    def setUp(self) -> None:
        self.request_path: str = '/posts/'

        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.auth_token: str = f'Bearer {auth_obj.jwt_token()}'

    def test_create_new_post(self):
        """
        The test checks happy way of creating a new post.
        """
        # create new post via endpoint
        request_data: dict = {
            'post_details': {
                'name': 'test post name',
                'description': 'super puper cool event',
                'type': TEST_POST_TYPE_PK
            },
            'address': {
                'country': 'Russia',
                'city': 'Kaliningrad',
                'street': 'Safronova',
                'house_no': '20',
                'floor': '3'
            }
        }
        response: Response = self.client.post(
            path=self.request_path,
            data=request_data,
            HTTP_AUTHORIZATION=self.auth_token,
            content_type=DEFAULT_CONTENT_TYPE
        )
        # check that response status code is 200 and response body contains success message
        assert response.status_code == HTTP_201_CREATED
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'New post has been successfully created.'

        # get new post from the DB and ensure that it has been saved correctly
        created_post: DbPostModel = DbPostModel.objects.get(id=response.data['id'])

        assert created_post.name == request_data['post_details']['name']
        assert created_post.description == request_data['post_details']['description']
        assert created_post.type == DbPostTypeModel.objects.get(id=TEST_POST_TYPE_PK)

        assert created_post.address.country == request_data['address']['country']
        assert created_post.address.city == request_data['address']['city']
        assert created_post.address.street == request_data['address']['street']
        assert created_post.address.house_no == request_data['address']['house_no']
        assert created_post.address.house_no == request_data['address']['house_no']
        assert created_post.address.floor == request_data['address']['floor']

    def test_create_new_post_invalid_request_body(self):
        """
        The test checks the case when request body is invalid.
        """
        # send request with invalid body
        invalid_request_data: dict = {
            'post_details': {
                'name': ['unknown key'],
                'invalid_attr': 'lalalaa',
                'type': {'key': 'value'}
            },
            'address': {
                'country': 'Russia',
                'city': 'Kaliningrad',
                'street': 'Safronova',
                'house_no': '20',
                'floor': '3'
            }
        }
        response: Response = self.client.post(
            path=self.request_path,
            data=invalid_request_data,
            HTTP_AUTHORIZATION=self.auth_token,
            content_type=DEFAULT_CONTENT_TYPE
        )

        # check that response status code is 400 and response body contains an error message
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            'status': 'error',
            'message': 'Request body is invalid.',
            'invalid_keys': ['post_details']
        }
