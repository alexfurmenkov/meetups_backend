from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from meetups_backend.models import DbUserModel, DbPostModel
from tests.utils.test_records_pks import TEST_POST_TYPE_PK
from tests.utils.test_constants import DEFAULT_CONTENT_TYPE


class TestMainUseCases(TestCase):
    """
    The class contains the integration tests
    that check the main use cases of the app.
    """
    fixtures = ['test_post_type.json', ]

    def test_sign_up_and_manage_post(self):
        """
        1. New user signs up and logs in.
        2. Then he uses his credentials to create a new post.
        3. After that, he wishes to change some details of the post.
        4. Finally, he decides to delete the post.
        """

        # create a new user
        new_user_data: dict = {
            'email': 'alex@mail.com',
            'password': 'test_password',
            'bio': 'Personal Info'
        }
        create_user_response: Response = self.client.post(
            path='/users/',
            data=new_user_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert create_user_response.status_code == HTTP_201_CREATED
        created_user_id: str = create_user_response.data['id']
        assert DbUserModel.objects.filter(id=created_user_id).exists()

        # log him in
        login_data: dict = {'email': 'alex@mail.com', 'password': 'test_password', }
        login_response: Response = self.client.post(
            path='/auth/login/',
            data=login_data,
            content_type=DEFAULT_CONTENT_TYPE
        )
        assert login_response.status_code == HTTP_200_OK
        auth_token: str = f'Bearer {login_response.data["auth_token"]}'

        # create a new post for this user
        new_post_data: dict = {
            'post_details': {
                'name': 'Rangers',
                'description': 'new basketball event',
                'type': TEST_POST_TYPE_PK
            },
            'address': {
                'country': 'Belgium',
                'city': 'Brussels',
                'street': 'Brusselstraat',
                'house_no': '55',
                'floor': '2'
            }
        }
        create_new_post_response: Response = self.client.post(
            path='/posts/',
            data=new_post_data,
            content_type=DEFAULT_CONTENT_TYPE,
            HTTP_AUTHORIZATION=auth_token
        )
        assert create_new_post_response.status_code == HTTP_201_CREATED
        created_post_id: str = create_new_post_response.data['id']
        assert DbPostModel.objects.filter(id=created_post_id).exists()

        # update post details
        update_post_data: dict = {
            'description': 'updated description',
            'name': 'Heroes',
        }
        update_post_response: Response = self.client.put(
            path=f'/posts/{created_post_id}/',
            data=update_post_data,
            content_type=DEFAULT_CONTENT_TYPE,
            HTTP_AUTHORIZATION=auth_token
        )
        assert update_post_response.status_code == HTTP_200_OK
        updated_post: DbPostModel = DbPostModel.objects.get(id=created_post_id)
        assert updated_post.description == update_post_data['description']
        assert updated_post.name == update_post_data['name']

        # delete the post
        delete_post_response: Response = self.client.delete(
            path=f'/posts/{created_post_id}/',
            content_type=DEFAULT_CONTENT_TYPE,
            HTTP_AUTHORIZATION=auth_token
        )
        assert delete_post_response.status_code == HTTP_200_OK
        assert not DbPostModel.objects.filter(id=created_post_id).exists()
