import uuid

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from meetups_backend.models import DbPostModel
from meetups_backend.serializers.model_serializers import DbPostModelSerializer
from meetups_backend.tools.auth_system_class import AuthSystem
from tests.utils.test_records_pks import TEST_POST_PK, TEST_USER_PASSWORD, TEST_USER_EMAIL


class TestGetPostsEndpoint(TestCase):
    """
    This class contains tests that check GET "/posts"
    and GET "/posts/{post_id}/" endpoints.
    """

    fixtures = ['test_user.json', 'test_post_type.json', 'test_post.json', 'test_post_address.json', ]

    def setUp(self) -> None:
        self.request_path: str = '/posts/'

        self.post: DbPostModel = DbPostModel.objects.get(pk=TEST_POST_PK)

        auth_obj: AuthSystem = AuthSystem.authenticate_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.jwt_token: str = f'Bearer {auth_obj.jwt_token()}'

    def test_list_posts(self):
        """
        Tests the happy scenario of listing posts.
        """
        response: Response = self.client.get(self.request_path, HTTP_AUTHORIZATION=self.jwt_token)
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'status': 'success',
            'message': 'Posts have been listed successfully.',
            'posts': DbPostModelSerializer([self.post], many=True).data
        }

    def test_get_post_by_id(self):
        """
        Tests the happy scenario of getting a post by id.
        """
        response: Response = self.client.get(f'{self.request_path}{self.post.id}/', HTTP_AUTHORIZATION=self.jwt_token)
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'status': 'success',
            'message': 'Post have been retrieved successfully.',
            'post': DbPostModelSerializer(self.post).data
        }

    def test_get_post_by_id_not_found(self):
        """
        Tests case when requested post is not found.
        Expected behavior is response with 404 status and error message.
        """
        not_found_post_id: str = str(uuid.uuid4())
        response: Response = self.client.get(
            f'{self.request_path}{not_found_post_id}/',
            HTTP_AUTHORIZATION=self.jwt_token
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data == {
            'status': 'error',
            'message': f'Resource with id {not_found_post_id} is not found.'
        }
