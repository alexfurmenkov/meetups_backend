import uuid

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from meetups_backend.models import DbPostModel
from meetups_backend.tools.auth_system_class import AuthSystem
from tests.utils.test_records_pks import TEST_POST_PK, TEST_USER_EMAIL, TEST_USER_PASSWORD


class TestUpdatePostAddressEndpoint(TestCase):
    """
    This class contains tests that check PUT "/posts/{post_id}/address/" endpoint.
    """

    fixtures = ['test_user.json', 'test_post_type.json', 'test_post.json', 'test_post_address.json', ]

    def setUp(self) -> None:
        self.request_path: str = '/posts/{post_id}/address/'

        self.post: DbPostModel = DbPostModel.objects.get(pk=TEST_POST_PK)

        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.jwt_token: str = f'Bearer {auth_obj.jwt_token()}'

    def test_update_post_address(self):
        """
        The test checks the happy scenario of updating
        an address of a post.
        """
        request_data: dict = {
            'country': 'Germany',
            'city': 'Berlin',
        }
        response: Response = self.client.put(
            path=self.request_path.format(post_id=self.post.id),
            data=request_data,
            HTTP_AUTHORIZATION=self.jwt_token,
            content_type='application/json'
        )
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'status': 'success',
            'message': f'Address of a post with id {self.post.id} has been updated successfully.'
        }

        updated_post: DbPostModel = DbPostModel.objects.get(id=self.post.id)
        assert updated_post.address.city == request_data['city']
        assert updated_post.address.country == request_data['country']

    def test_update_post_address_not_found(self):
        """
        The test checks the case when requested post is not found.
        """
        request_data: dict = {}
        post_id: str = str(uuid.uuid4())
        response: Response = self.client.put(
            path=self.request_path.format(post_id=post_id),
            data=request_data,
            HTTP_AUTHORIZATION=self.jwt_token,
            content_type='application/json'
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data == {
            'status': 'error',
            'message': f'Resource with id {post_id} is not found.'
        }

    def test_update_post_address_invalid_request(self):
        """
        The tests checks the case when request body is invalid.
        """
        request_data: dict = {
            'country': {'invalid_key': 'invalid_value'},
        }
        response: Response = self.client.put(
            path=self.request_path.format(post_id=self.post.id),
            data=request_data,
            HTTP_AUTHORIZATION=self.jwt_token,
            content_type='application/json'
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            'status': 'error',
            'message': 'Request body is invalid.',
            'invalid_keys': ['country']
        }
