import uuid

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from meetups_backend.models import DbPostModel, DbUserModel
from meetups_backend.tools.auth_system_class import AuthSystem
from tests.utils.test_records_pks import TEST_POST_PK, TEST_USER_EMAIL, TEST_USER_PASSWORD, \
    TEST_USER_PK


class TestDeletePostEndpoint(TestCase):
    """
    This class contains tests that check DELETE "/posts/{post_id}" endpoint.
    """

    fixtures = ['test_user.json', 'test_post_type.json', 'test_post.json', 'test_post_address.json', ]

    def setUp(self) -> None:
        self.request_path: str = '/posts/'

        self.user: DbUserModel = DbUserModel.objects.get(pk=TEST_USER_PK)
        self.post: DbPostModel = DbPostModel.objects.get(pk=TEST_POST_PK)

        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.jwt_token: str = f'Bearer {auth_obj.jwt_token()}'

    def test_delete_post(self):
        """
        The test checks happy way of deleting a post.
        """
        response: Response = self.client.delete(
            path=f'{self.request_path}{self.post.id}/',
            HTTP_AUTHORIZATION=self.jwt_token,
            content_type='application/json'
        )

        # check response format
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'status': 'success',
            'message': f'Post with id {self.post.id} has been deleted successfully.'
        }

        # ensure that DB record has been deleted
        assert not DbPostModel.objects.filter(user=self.user, id=self.post.id).exists()

    def test_delete_post_not_found(self):
        """
        The test checks the case when requested post is not found.
        """
        post_id: str = str(uuid.uuid4())
        response: Response = self.client.delete(
            path=f'{self.request_path}{post_id}/',
            HTTP_AUTHORIZATION=self.jwt_token,
            content_type='application/json'
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data == {
            'status': 'error',
            'message': f'Resource with id {post_id} is not found.'
        }
